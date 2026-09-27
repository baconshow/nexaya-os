"""Testes do checar_os.py com um OS mínimo montado em pasta temporária.

Rodar da pasta scripts/: python -m unittest discover -s testes -v
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import checar_os  # noqa: E402

REPO = Path(__file__).resolve().parents[4]
EXEMPLO = REPO / "exemplo"

HUB = """---
os: hub
depto: Sistema
resumo: teste
---

# OS

## Departamentos

- [Casa](Casa/CLAUDE.md) — casa
- [Sistema](Sistema/CLAUDE.md) — o OS
"""

CASA = """---
os: departamento
depto: Casa
resumo: casa
---

# Casa

## Projeto

- [Horta](horta/) — horta. Ler primeiro: [PROXIMO.md](horta/PROXIMO.md)
- [Sumido](sumido/) — pasta que não existe
- [Segredo](horta/.env) — não pode ser link

## Apps

- `horta-web` — app da horta
- `fantasma` — app que não está no registro

Exemplo entre crases não é link: `[x](nao-existe.md)`.

```markdown
- [Dentro de bloco](tambem-nao-existe.md)
```
"""

SISTEMA = """---
os: departamento
depto: Sistema
---

# Sistema

## Rotinas

- `faxina-semanal` — faxina
"""


def escrever(caminho: Path, texto: str) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding="utf-8")


def montar_os(raiz: Path) -> Path:
    escrever(raiz / "CLAUDE.md", HUB)
    escrever(raiz / "Casa" / "CLAUDE.md", CASA)
    escrever(raiz / "Casa" / "horta" / "PROXIMO.md", "# PROXIMO\n\n## Estado atual (2020-01-01)\n")
    escrever(raiz / "Sistema" / "CLAUDE.md", SISTEMA)
    escrever(raiz / "Orfao" / "CLAUDE.md", "# fora do hub\n")
    escrever(raiz / "solto.txt", "sobra")
    memoria = raiz / "Sistema" / "memoria"
    escrever(memoria / "MEMORY.md", "# Memory Index\n\n## Casa\n- [A](a.md) — a\n- [Z](z.md) — some\n\n## Diversos\n")
    escrever(memoria / "a.md", "---\nname: a\n---\nVer [[b]] e [[nao-existe]].\n")
    escrever(memoria / "b.md", "---\nname: b\n---\nsem linha no índice\n")
    escrever(memoria / "a-NOTEBOOK.md", "cópia de conflito\n")
    escrever(memoria / "MEMORY-NOTEBOOK.md", "cópia do índice\n")
    apps = {"apps": [
        {"id": "horta-web", "pasta": "{OS_ROOT}/Casa/horta", "porta": 5601},
        {"id": "outra", "pasta": "{OS_ROOT}/nao-existe", "porta": 5601},
    ]}
    escrever(raiz / "Sistema" / "apps.json", json.dumps(apps))
    escrever(raiz / "Sistema" / "rotinas.json", "{ isto não é json")
    return memoria


def problemas(itens: list) -> str:
    return " | ".join(json.dumps(i, ensure_ascii=False) for i in itens)


class TestOSComDefeitos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        raiz = Path(cls.tmp.name)
        memoria = montar_os(raiz)
        cls.achados = checar_os.checar(raiz, memoria, None, 7)["achados"]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_link_quebrado_fora_de_crase_e_de_bloco(self):
        alvos = [i["alvo"] for i in self.achados["links_quebrados"]]
        self.assertIn("sumido/", alvos)
        self.assertNotIn("nao-existe.md", alvos)
        self.assertNotIn("tambem-nao-existe.md", alvos)

    def test_link_sensivel_e_separado(self):
        self.assertEqual([i["alvo"] for i in self.achados["links_sensiveis"]], ["horta/.env"])

    def test_convencoes(self):
        texto = problemas(self.achados["convencoes"])
        self.assertIn("Orfao/CLAUDE.md", texto)
        self.assertIn("parece a seção reservada 'projetos'", texto)
        self.assertIn("sem resumo", texto)

    def test_memoria(self):
        texto = problemas(self.achados["memoria"])
        self.assertIn("linha sem arquivo", texto)
        self.assertIn("b.md", texto)
        self.assertIn("[[nao-existe]]", texto)
        self.assertNotIn("[[b]]", texto)
        self.assertIn("a-NOTEBOOK.md", texto)
        self.assertIn("MEMORY-NOTEBOOK.md", texto)
        self.assertIn("Diversos", texto)

    def test_handoff_parado_pela_data_escrita(self):
        horta = [i for i in self.achados["handoffs"] if i["arquivo"] == "Casa/horta/PROXIMO.md"]
        self.assertEqual(len(horta), 1)
        self.assertTrue(horta[0]["parado"])
        self.assertEqual(horta[0]["data_no_arquivo"], "2020-01-01")

    def test_arquivo_solto(self):
        self.assertEqual([i["arquivo"] for i in self.achados["arquivos_soltos"]], ["solto.txt"])

    def test_registros(self):
        texto = problemas(self.achados["registros"])
        self.assertIn("porta 5601 repetida", texto)
        self.assertIn("pasta não existe", texto)
        self.assertIn("`fantasma`", texto)
        self.assertIn("rotinas.json", texto)
        self.assertIn("JSON inválido", texto)


class TestFiltrosDeCaminho(unittest.TestCase):
    def test_sensivel(self):
        for nome in (".env", ".env.local", "chave.txt", "Senhas.xlsx", "api_token.md", "cert.pfx"):
            self.assertTrue(checar_os.eh_sensivel(nome), nome)
        for nome in ("CLAUDE.md", "PROXIMO.md", "painel-vendas/"):
            self.assertFalse(checar_os.eh_sensivel(nome), nome)

    def test_url_e_ancora_nao_sao_links_de_arquivo(self):
        self.assertIsNone(checar_os.alvo_do_link("https://exemplo.invalid/x"))
        self.assertIsNone(checar_os.alvo_do_link("#secao"))
        self.assertEqual(checar_os.alvo_do_link("<pasta com espaço/>"), "pasta com espaço/")
        self.assertEqual(checar_os.alvo_do_link("a.md#secao"), "a.md")


HUB_COM_PAINEL = HUB.replace("- [Casa](Casa/CLAUDE.md) — casa\n", "") + """
## Painel

O painel do Nexaya OS Pro mostra o grafo do OS. Abra com `Sistema/painel/abrir-painel.bat`.
"""

SISTEMA_COM_PAINEL = """---
os: departamento
depto: Sistema
resumo: o OS
---

# Sistema

## Apps

- `painel-os` — o painel do Nexaya OS Pro em http://127.0.0.1:5400
"""

# a entrada que o INSTALAR.md do Nexaya OS Pro manda pôr no apps.json
ENTRADA_PAINEL = {
    "id": "painel-os", "nome": "Painel do OS", "depto": "Sistema",
    "pasta": "{OS_ROOT}/Sistema/painel", "comando": "python servir.py",
    "porta": 5400, "url": "http://127.0.0.1:5400", "maquina": "ambas",
    "descricao": "Painel do Nexaya OS Pro",
}


class TestOSComOPainelDoPro(unittest.TestCase):
    """O registro do painel que o INSTALAR.md do Pro faz precisa passar limpo na faxina."""

    def montar(self, raiz: Path, apps: list) -> dict:
        escrever(raiz / "CLAUDE.md", HUB_COM_PAINEL)
        escrever(raiz / "Sistema" / "CLAUDE.md", SISTEMA_COM_PAINEL)
        escrever(raiz / "Sistema" / "painel" / "servir.py", "# painel\n")
        escrever(raiz / "Sistema" / "apps.json", json.dumps({"apps": apps}))
        memoria = raiz / "Sistema" / "memoria"
        escrever(memoria / "MEMORY.md", "# Memory Index\n")
        return checar_os.checar(raiz, memoria, None, 7)["achados"]

    def test_painel_registrado_como_o_instalar_manda(self):
        with tempfile.TemporaryDirectory() as tmp:
            achados = self.montar(Path(tmp), [ENTRADA_PAINEL])
        for chave in ("links_quebrados", "convencoes", "registros"):
            self.assertEqual(achados[chave], [], f"{chave}: {problemas(achados[chave])}")

    def test_painel_citado_sem_registro_e_achado(self):
        with tempfile.TemporaryDirectory() as tmp:
            achados = self.montar(Path(tmp), [])
        self.assertIn("`painel-os` citado em ## apps mas ausente de apps.json", problemas(achados["registros"]))


@unittest.skipUnless((EXEMPLO / "CLAUDE.md").is_file(), "exemplo/ não encontrado")
class TestExemploDoRepositorio(unittest.TestCase):
    def test_exemplo_sem_link_quebrado_nem_problema_de_convencao(self):
        resultado = checar_os.checar(EXEMPLO, EXEMPLO / "Sistema" / "memoria", None, 7)
        achados = resultado["achados"]
        self.assertEqual(resultado["departamentos"], ["Trabalho", "Empresa", "Estudos", "Pessoal", "Sistema"])
        for chave in ("links_quebrados", "links_sensiveis", "convencoes", "memoria",
                      "arquivos_soltos", "registros"):
            self.assertEqual(achados[chave], [], f"{chave}: {problemas(achados[chave])}")


if __name__ == "__main__":
    unittest.main()


class TestMemoriaPadrao(unittest.TestCase):
    """A memória global do usuário só vale para o OS onde ela mora."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.casa = base / "casa"
        self.os_checado = base / "outro-os"
        (self.os_checado / "Sistema" / "memoria").mkdir(parents=True)
        (self.casa / ".claude").mkdir(parents=True)
        self.global_ = base / "meu-os" / "memoria"
        self.global_.mkdir(parents=True)
        (self.casa / ".claude" / "settings.json").write_text(
            json.dumps({"autoMemoryDirectory": str(self.global_)}), encoding="utf-8")
        self.env_antigo = {k: os.environ.get(k) for k in ("HOME", "USERPROFILE", "AGENTIC_OS_MEMORY_DIR")}
        os.environ["HOME"] = os.environ["USERPROFILE"] = str(self.casa)
        os.environ.pop("AGENTIC_OS_MEMORY_DIR", None)

    def tearDown(self):
        for chave, valor in self.env_antigo.items():
            if valor is None:
                os.environ.pop(chave, None)
            else:
                os.environ[chave] = valor
        self.tmp.cleanup()

    def test_outro_os_usa_a_propria_memoria(self):
        self.assertEqual(checar_os.memoria_padrao(self.os_checado), self.os_checado / "Sistema" / "memoria")

    def test_o_proprio_os_usa_a_memoria_global(self):
        self.assertEqual(checar_os.memoria_padrao(self.global_.parent).resolve(), self.global_.resolve())
