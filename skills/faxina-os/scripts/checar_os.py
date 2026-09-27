"""Checagens mecânicas da faxina do Nexaya OS. Só lê; nunca altera nada.

Uso:
    python checar_os.py <raiz do OS> [--memoria PASTA] [--dias 7] [--formato json|md]
                        [--perfil-origem PREFIXO] [--falhar-se-quebrado]

Lê o hub, os roteadores dos departamentos, os .md de primeiro nível com
frontmatter "os:", o índice de memória, os registros apps.json e rotinas.json,
e a data dos PROXIMO.md. Não abre arquivo com nome sensível (.env, chaves,
certificados, senha, token...): no máximo confere se o caminho existe.
Só biblioteca padrão; Python 3.10+.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import unquote

LIMITE_ROTEADOR = 150
LIMITE_MEMORY_MD = 200
LIMITE_MEMORIA_BYTES = 10 * 1024
MAX_BYTES_LEITURA = 512 * 1024
PULAR_PASTAS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
                ".next", ".cache", "target"}
SECOES = {"departamentos", "ler primeiro", "projetos", "skills", "referencias", "apps",
          "rotinas", "regras", "pendencias", "maquinas"}
QUASE_SECOES = {"projeto": "projetos", "skill": "skills", "referencia": "referencias",
                "app": "apps", "rotina": "rotinas", "regra": "regras", "pendencia": "pendencias",
                "maquina": "maquinas", "departamento": "departamentos", "leia primeiro": "ler primeiro",
                "ler antes": "ler primeiro", "read first": "ler primeiro", "projects": "projetos",
                "references": "referencias", "routines": "rotinas", "rules": "regras",
                "departments": "departamentos", "machines": "maquinas"}
TIPOS_OS = {"hub", "departamento", "memoria", "indice", "referencia"}
RAIZ_PERMITIDOS = {"claude.md", "readme.md", "agents.md", ".gitignore", ".ignore", "desktop.ini",
                   ".ds_store", "license", "license.md"}

RE_SENSIVEL = re.compile(
    r"\.env|\.pfx|\.p12|\.key$|\.pem|\.jks|\.kdbx|id_rsa|id_ed25519|serviceaccount|client_secret"
    r"|chave|senha|password|passwd|secret|token|credencia|credential|vault|contrato|holerite"
    r"|payslip|contract", re.IGNORECASE)
RE_LINK = re.compile(r"(?<!!)\[([^\]\n]*)\]\((<[^>\n]*>|[^)\n]*)\)")
RE_CRASE = re.compile(r"`[^`\n]+`")
RE_WIKILINK = re.compile(r"\[\[([^\]|#\n]+)(?:#[^\]|\n]*)?(?:\|[^\]\n]*)?\]\]")
RE_URL = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:(//|[^\\/])")
RE_ABSOLUTO = re.compile(r"^([a-zA-Z]:[\\/]|\\\\|/|~|\{(OS_ROOT|HOME|MEMORY_DIR)\})")
RE_ITEM_CRASE = re.compile(r"^\s*[-*+]\s+`([^`\n]+)`")
RE_DATA = re.compile(r"\b(20\d\d-[01]\d-[0-3]\d)\b")
RE_CONFLITO = re.compile(r"^(-[A-Z0-9][A-Z0-9_-]*|\s\(\d+\)|\s\d+|.*[Cc]onfli[ct].*)$")


def sem_acento(texto: str) -> str:
    base = unicodedata.normalize("NFKD", texto)
    base = "".join(c for c in base if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", base).strip(" :").casefold()


def eh_sensivel(caminho) -> bool:
    return bool(RE_SENSIVEL.search(str(caminho).replace("\\", "/")))


def ler(caminho: Path) -> str:
    """Texto de um arquivo não sensível, até 512 KB. Arquivo sensível vira texto vazio."""
    if eh_sensivel(caminho):
        return ""
    with open(caminho, "rb") as arquivo:
        return arquivo.read(MAX_BYTES_LEITURA).decode("utf-8", errors="replace").lstrip("﻿")


def frontmatter(linhas: list) -> dict | None:
    if not linhas or linhas[0].strip() != "---":
        return None
    dados = {}
    for linha in linhas[1:80]:
        if linha.strip() == "---":
            return dados
        if ":" in linha and not linha[:1].isspace():
            chave, valor = linha.split(":", 1)
            dados[chave.strip().casefold()] = valor.strip().strip("\"'")
    return None


def linhas_uteis(texto: str, limpar: bool = True):
    """(número, linha) fora de blocos de código; com limpar, sem os trechos entre crases."""
    dentro = False
    for numero, linha in enumerate(texto.splitlines(), 1):
        if linha.lstrip().startswith(("```", "~~~")):
            dentro = not dentro
            continue
        if not dentro:
            yield numero, RE_CRASE.sub(lambda m: " " * len(m.group(0)), linha) if limpar else linha


def alvo_do_link(bruto: str) -> str | None:
    alvo = bruto.strip()
    if alvo.startswith("<") and alvo.endswith(">"):
        alvo = alvo[1:-1].strip()
    elif ' "' in alvo:
        alvo = alvo.split(' "', 1)[0].strip()
    if not alvo or alvo.startswith("#") or RE_URL.match(alvo) and not re.match(r"^[a-zA-Z]:[\\/]", alvo):
        return None
    alvo = unquote(alvo) if "%" in alvo else alvo
    return alvo.split("#", 1)[0] or None


class Contexto:
    def __init__(self, raiz: Path, memoria: Path | None, perfil_origem: str | None, dias: int):
        self.raiz = raiz
        self.memoria = memoria
        self.home = Path.home()
        self.perfil_origem = (perfil_origem or "").rstrip("\\/")
        self.limite_idade = time.time() - dias * 86400
        self.dias = dias

    def resolver(self, alvo: str, base: Path) -> Path:
        texto = alvo.replace("{OS_ROOT}", str(self.raiz)).replace("{HOME}", str(self.home))
        if self.memoria is not None:
            texto = texto.replace("{MEMORY_DIR}", str(self.memoria))
        if texto.startswith("~"):
            texto = str(self.home) + texto[1:]
        perfil = self.perfil_origem.replace("\\", "/").casefold()
        if perfil and texto.replace("\\", "/").casefold().startswith(perfil):
            texto = str(self.home) + texto[len(self.perfil_origem):]
        if os.sep == "/":
            texto = texto.replace("\\", "/")
        caminho = Path(texto)
        return caminho if RE_ABSOLUTO.match(alvo) else base / caminho


def links_do_texto(texto: str) -> list:
    saida = []
    for numero, linha in linhas_uteis(texto):
        for m in RE_LINK.finditer(linha):
            alvo = alvo_do_link(m.group(2))
            if alvo:
                saida.append((numero, alvo))
    return saida


def secoes(texto: str) -> list:
    """[(título, [linhas do corpo])] das seções ##, fora de blocos de código."""
    saida = []
    for _numero, linha in linhas_uteis(texto, limpar=False):
        if linha.startswith("## "):
            saida.append((linha[3:].strip(), []))
        elif saida:
            saida[-1][1].append(linha)
    return saida


def departamentos(ctx: Contexto, hub_texto: str, achados: dict) -> list:
    nomes = []
    for titulo, corpo in secoes(hub_texto):
        if sem_acento(titulo) != "departamentos":
            continue
        for _numero, alvo in links_do_texto("\n".join(corpo)):
            destino = ctx.resolver(alvo, ctx.raiz)
            pasta = destino.parent if destino.suffix.casefold() == ".md" else destino
            nomes.append(pasta.name)
    if not nomes:
        achados["convencoes"].append({"arquivo": "CLAUDE.md", "problema": "hub sem seção ## Departamentos com links"})
    if "Sistema" not in nomes:
        achados["convencoes"].append({"arquivo": "CLAUDE.md", "problema": "departamento Sistema ausente do hub"})
    listados = {n.casefold() for n in nomes}
    for pasta in sorted(p for p in ctx.raiz.iterdir() if p.is_dir() and not p.name.startswith(".")):
        if (pasta / "CLAUDE.md").is_file() and pasta.name.casefold() not in listados:
            achados["convencoes"].append({"arquivo": f"{pasta.name}/CLAUDE.md",
                                          "problema": "pasta com CLAUDE.md que não está em ## Departamentos"})
    return nomes


def documentos(ctx: Contexto, deptos: list) -> list:
    """(caminho, depto, é_roteador) do hub, roteadores e .md de primeiro nível com os:."""
    saida = [(ctx.raiz / "CLAUDE.md", None, True)]
    for depto in deptos:
        pasta = ctx.raiz / depto
        saida.append((pasta / "CLAUDE.md", depto, True))
        if not pasta.is_dir():
            continue
        for arquivo in sorted(pasta.glob("*.md")):
            if arquivo.name.casefold() == "claude.md" or eh_sensivel(arquivo):
                continue
            fm = frontmatter(ler(arquivo).splitlines()[:80])
            if fm is not None and "os" in fm:
                saida.append((arquivo, depto, False))
    return saida


def checar_documento(ctx: Contexto, caminho: Path, depto, roteador: bool, achados: dict, usados: dict):
    rel = caminho.relative_to(ctx.raiz).as_posix()
    if not caminho.is_file():
        achados["convencoes"].append({"arquivo": rel, "problema": "arquivo não existe"})
        return
    texto = ler(caminho)
    linhas = texto.splitlines()
    fm = frontmatter(linhas)
    if fm is None or "os" not in fm:
        achados["convencoes"].append({"arquivo": rel, "problema": "sem frontmatter os:"})
    else:
        if fm.get("os") not in TIPOS_OS:
            achados["convencoes"].append({"arquivo": rel, "problema": f"os: '{fm.get('os')}' fora do contrato"})
        if depto and fm.get("depto", "").casefold() != depto.casefold():
            achados["convencoes"].append({"arquivo": rel, "problema": f"depto: '{fm.get('depto')}' diferente da pasta"})
        if not fm.get("resumo"):
            achados["convencoes"].append({"arquivo": rel, "problema": "frontmatter sem resumo:"})
    if roteador and depto and len(linhas) > LIMITE_ROTEADOR:
        achados["convencoes"].append({"arquivo": rel, "problema": f"roteador com {len(linhas)} linhas (limite ~{LIMITE_ROTEADOR})"})
    for titulo, corpo in secoes(texto):
        chave = sem_acento(titulo)
        if chave not in SECOES and chave in QUASE_SECOES:
            achados["convencoes"].append({"arquivo": rel, "problema": f"título '## {titulo}' parece a seção reservada '{QUASE_SECOES[chave]}'"})
        if chave in ("apps", "rotinas"):
            for linha in corpo:
                m = RE_ITEM_CRASE.match(linha)
                if m:
                    usados[chave].setdefault(m.group(1).strip(), rel)
    for numero, alvo in links_do_texto(texto):
        destino = ctx.resolver(alvo, caminho.parent)
        if eh_sensivel(alvo):
            achados["links_sensiveis"].append({"arquivo": rel, "linha": numero, "alvo": alvo})
        elif not destino.exists():
            achados["links_quebrados"].append({"arquivo": rel, "linha": numero, "alvo": alvo})
        elif destino.name.casefold() == "proximo.md":
            usados["proximos"].add(os.path.normpath(str(destino)))


def checar_memoria(ctx: Contexto, deptos: list, achados: dict):
    pasta = ctx.memoria
    if pasta is None or not pasta.is_dir():
        achados["memoria"].append({"problema": "pasta de memória não encontrada", "detalhe": str(pasta)})
        return
    arquivos = {p.name.casefold(): p for p in pasta.glob("*.md") if not eh_sensivel(p)}
    indice = pasta / "MEMORY.md"
    if not indice.is_file():
        achados["memoria"].append({"problema": "MEMORY.md não existe", "detalhe": str(indice)})
        return
    texto = ler(indice)
    if len(texto.splitlines()) > LIMITE_MEMORY_MD:
        achados["memoria"].append({"problema": "MEMORY.md longo", "detalhe": f"{len(texto.splitlines())} linhas"})
    nomes_deptos = {d.casefold() for d in deptos}
    for titulo, _corpo in secoes(texto):
        if sem_acento(titulo) not in nomes_deptos:
            achados["memoria"].append({"problema": "seção do MEMORY.md que não é departamento", "detalhe": titulo})
    no_indice = set()
    for numero, alvo in links_do_texto(texto):
        destino = ctx.resolver(alvo, pasta)
        no_indice.add(destino.name.casefold())
        if not destino.exists():
            achados["memoria"].append({"problema": "linha sem arquivo", "detalhe": f"MEMORY.md:{numero} {alvo}"})
    _checar_arquivos_memoria(arquivos, no_indice, achados)


def _checar_arquivos_memoria(arquivos: dict, no_indice: set, achados: dict):
    stems = {p.stem for p in arquivos.values()}
    for chave, arquivo in sorted(arquivos.items()):
        if arquivo.name.upper().startswith("MEMORY"):
            if chave != "memory.md":
                achados["memoria"].append({"problema": "possível cópia de conflito do índice", "detalhe": arquivo.name})
            continue
        if chave not in no_indice:
            achados["memoria"].append({"problema": "memória sem linha no MEMORY.md", "detalhe": arquivo.name})
        if arquivo.stat().st_size > LIMITE_MEMORIA_BYTES:
            achados["memoria"].append({"problema": "memória grande (>10 KB)", "detalhe": arquivo.name})
        for outro in stems:
            resto = arquivo.stem[len(outro):]
            if outro != arquivo.stem and arquivo.stem.startswith(outro) and RE_CONFLITO.match(resto):
                achados["memoria"].append({"problema": "possível cópia de conflito", "detalhe": arquivo.name})
        for alvo in RE_WIKILINK.findall(ler(arquivo)):
            nome = alvo.strip().casefold()
            nome = nome if nome.endswith(".md") else nome + ".md"
            if nome not in arquivos:
                achados["memoria"].append({"problema": "[[link]] quebrado", "detalhe": f"{arquivo.name} -> [[{alvo.strip()}]]"})


def checar_handoffs(ctx: Contexto, apontados: set, achados: dict):
    """PROXIMO.md dentro da raiz (varredura) e os apontados pelos roteadores fora dela."""
    encontrados = set()
    for pasta, subpastas, nomes in os.walk(ctx.raiz):
        atual = Path(pasta)
        subpastas[:] = [s for s in subpastas if s not in PULAR_PASTAS
                        and not (atual == ctx.raiz / "Sistema" and s in ("painel", "dados"))]
        encontrados.update(os.path.normpath(str(atual / n)) for n in nomes if n.casefold() == "proximo.md")
    for caminho in sorted(encontrados | set(apontados)):
        arquivo = Path(caminho)
        mtime = arquivo.stat().st_mtime
        try:
            nome = arquivo.relative_to(ctx.raiz).as_posix()
        except ValueError:
            nome = str(arquivo)
        escrita = data_escrita(ler(arquivo))
        referencia = escrita if escrita is not None else mtime
        achados["handoffs"].append({
            "arquivo": nome,
            "modificado": time.strftime("%Y-%m-%d", time.localtime(mtime)),
            "data_no_arquivo": time.strftime("%Y-%m-%d", time.localtime(escrita)) if escrita else None,
            "parado": referencia < ctx.limite_idade,
        })


def data_escrita(texto: str) -> float | None:
    """Primeira data AAAA-MM-DD das 30 primeiras linhas (o "Estado atual" do PROXIMO.md)."""
    for linha in texto.splitlines()[:30]:
        m = RE_DATA.search(linha)
        if m:
            try:
                return time.mktime(time.strptime(m.group(1), "%Y-%m-%d"))
            except (ValueError, OverflowError):
                return None
    return None


def checar_raiz(ctx: Contexto, achados: dict):
    for arquivo in sorted(p for p in ctx.raiz.iterdir() if p.is_file()):
        if arquivo.name.casefold() in RAIZ_PERMITIDOS:
            continue
        achados["arquivos_soltos"].append({
            "arquivo": arquivo.name,
            "novo": arquivo.stat().st_mtime >= ctx.limite_idade,
        })


def _carregar_registro(caminho: Path, chave: str, achados: dict) -> list:
    if not caminho.is_file():
        return []
    try:
        dados = json.loads(ler(caminho))
    except ValueError as erro:
        achados["registros"].append({"arquivo": caminho.name, "problema": f"JSON inválido: {erro}"})
        return []
    lista = dados.get(chave, []) if isinstance(dados, dict) else dados
    return [d for d in lista if isinstance(d, dict)] if isinstance(lista, list) else []


def checar_registros(ctx: Contexto, usados: dict, achados: dict):
    sistema = ctx.raiz / "Sistema"
    apps = _carregar_registro(sistema / "apps.json", "apps", achados)
    portas = {}
    for app in apps:
        id_ = str(app.get("id") or "")
        porta = app.get("porta")
        if isinstance(porta, int) and porta > 0:
            if porta in portas:
                achados["registros"].append({"arquivo": "apps.json", "problema": f"porta {porta} repetida: {portas[porta]} e {id_}"})
            portas.setdefault(porta, id_)
        pasta = app.get("pasta")
        if isinstance(pasta, str) and pasta.strip() and not ctx.resolver(pasta, ctx.raiz).exists():
            achados["registros"].append({"arquivo": "apps.json", "problema": f"{id_}: pasta não existe ({pasta})"})
    rotinas = _carregar_registro(sistema / "rotinas.json", "rotinas", achados)
    for tipo, registro, arquivo in (("apps", apps, "apps.json"), ("rotinas", rotinas, "rotinas.json")):
        ids = {str(r.get("id")) for r in registro if r.get("id")}
        for id_, onde in sorted(usados[tipo].items()):
            if id_ not in ids:
                achados["registros"].append({"arquivo": onde, "problema": f"`{id_}` citado em ## {tipo} mas ausente de {arquivo}"})
        for id_ in sorted(ids - set(usados[tipo])):
            achados["registros"].append({"arquivo": arquivo, "problema": f"`{id_}` registrado mas não citado em nenhum ## {tipo}"})


def _dentro(caminho: Path, raiz: Path) -> bool:
    try:
        caminho.resolve().relative_to(raiz.resolve())
        return True
    except (OSError, ValueError):
        return False


def memoria_padrao(raiz: Path) -> Path | None:
    """AGENTIC_OS_MEMORY_DIR; senão o autoMemoryDirectory do ~/.claude/settings.json,
    se ele estiver dentro deste OS; senão <raiz>/Sistema/memoria; senão o global.

    Checar um OS que não é o seu (o exemplo, o de outra pessoa) não pode ler a sua
    memória global: por isso ela só vale quando mora dentro da raiz checada.
    """
    variavel = os.environ.get("AGENTIC_OS_MEMORY_DIR", "").strip()
    if variavel:
        return Path(os.path.expanduser(variavel)).resolve()
    global_ = None
    try:
        dados = json.loads((Path.home() / ".claude" / "settings.json").read_text(encoding="utf-8"))
        valor = dados.get("autoMemoryDirectory") if isinstance(dados, dict) else None
        if isinstance(valor, str) and valor.strip():
            global_ = Path(os.path.expanduser(valor))
    except (OSError, ValueError):
        pass
    if global_ is not None and _dentro(global_, raiz):
        return global_
    local = raiz / "Sistema" / "memoria"
    if local.is_dir():
        return local
    return global_


def perfil_do_painel(raiz: Path) -> str | None:
    try:
        dados = json.loads((raiz / "Sistema" / "painel" / "config.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    valor = dados.get("perfil_origem") if isinstance(dados, dict) else None
    return valor if isinstance(valor, str) and valor.strip() else None


def checar(raiz: Path, memoria: Path | None, perfil_origem: str | None = None, dias: int = 7) -> dict:
    ctx = Contexto(raiz, memoria, perfil_origem, dias)
    achados = {k: [] for k in ("links_quebrados", "links_sensiveis", "convencoes", "memoria",
                               "handoffs", "arquivos_soltos", "registros")}
    hub = raiz / "CLAUDE.md"
    if not hub.is_file():
        achados["convencoes"].append({"arquivo": "CLAUDE.md", "problema": "hub não existe"})
        return {"raiz": str(raiz), "memoria": str(memoria), "achados": achados}
    deptos = departamentos(ctx, ler(hub), achados)
    usados = {"apps": {}, "rotinas": {}, "proximos": set()}
    for caminho, depto, roteador in documentos(ctx, deptos):
        checar_documento(ctx, caminho, depto, roteador, achados, usados)
    checar_memoria(ctx, deptos, achados)
    checar_handoffs(ctx, usados["proximos"], achados)
    checar_raiz(ctx, achados)
    checar_registros(ctx, usados, achados)
    return {"raiz": str(raiz), "memoria": str(memoria), "departamentos": deptos, "achados": achados}


def em_markdown(resultado: dict) -> str:
    achados = resultado["achados"]
    saida = [f"# Faxina — {resultado['raiz']}", "", f"Memória: {resultado['memoria']}", ""]
    for chave, itens in achados.items():
        if chave == "handoffs":
            itens = [i for i in itens if i["parado"]]
        saida.append(f"## {chave.replace('_', ' ').capitalize()} ({len(itens)})")
        saida.extend(f"- {json.dumps(i, ensure_ascii=False)}" for i in itens)
        saida.append("")
    return "\n".join(saida)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Checagens mecânicas da faxina do Nexaya OS (só leitura).")
    parser.add_argument("raiz", nargs="?", default=os.environ.get("AGENTIC_OS_ROOT") or os.getcwd())
    parser.add_argument("--memoria", help="pasta de memória (padrão: autoMemoryDirectory, senão Sistema/memoria)")
    parser.add_argument("--dias", type=int, default=7, help="idade para marcar PROXIMO.md parado")
    parser.add_argument("--perfil-origem", help="prefixo de perfil dos caminhos absolutos (padrão: o do config do painel)")
    parser.add_argument("--formato", choices=("json", "md"), default="json")
    parser.add_argument("--falhar-se-quebrado", action="store_true", help="código de saída 1 se houver link quebrado")
    args = parser.parse_args(argv)
    raiz = Path(args.raiz).resolve()
    memoria = Path(args.memoria).resolve() if args.memoria else memoria_padrao(raiz)
    resultado = checar(raiz, memoria, args.perfil_origem or perfil_do_painel(raiz), args.dias)
    texto = em_markdown(resultado) if args.formato == "md" else json.dumps(resultado, ensure_ascii=False, indent=2)
    sys.stdout.reconfigure(encoding="utf-8")
    print(texto)
    quebrados = resultado["achados"]["links_quebrados"] or any(
        m["problema"] in ("linha sem arquivo", "[[link]] quebrado") for m in resultado["achados"]["memoria"])
    return 1 if args.falhar_se_quebrado and quebrados else 0


if __name__ == "__main__":
    sys.exit(main())
