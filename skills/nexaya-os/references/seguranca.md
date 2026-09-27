# Security and privacy

Applies to every step. The OS is a map of the user's digital life; it must
never become the place where their secrets leak.

## Never open

Record that these exist (path only), never read their contents:

- Environment and secret files: `.env`, `.env.*`, `*.pfx`, `*.p12`, `*.key`,
  `*.pem`, `*.crt` with a private key next to it, `*.jks`, `*.kdbx`,
  `id_rsa*`, `id_ed25519*`, `*serviceAccount*.json`, `client_secret*.json`,
  `.npmrc` and `.pypirc` with tokens, `credentials*`.
- Names containing: key, password, passwd, secret, token, credential, vault,
  login, account, oauth, or the same words in the user's language (for
  Portuguese: chave, senha, conta, credencial).
- Personal documents: payslips, tax forms, bank statements, receipts,
  contracts, NDAs, IDs and passports, medical records, personal photos.
- Folders the user named as private in the interview.
- In cloud-synced folders: binaries (they may be online-only placeholders and
  opening them triggers a download).

`~/.claude/history.jsonl` and session transcripts can contain secrets that
were pasted once. Search them with grep for counts only; never print lines
that match key patterns.

## Never write

- No secret value anywhere: not in routers, not in memory, not in
  `SEGURANCA.md`, not in the chat. Not even the first characters.
- No health, financial or legal detail about anyone.
- No personal data of third parties; use a role ("the client").
- Sensitive paths are cited between backticks, never as links, so the panel's
  graph never points at them.

## Risk patterns to report

When the inventory finds these, add them to `Sistema/SEGURANCA.md`:

| Level | Pattern | Usual action for the user |
|---|---|---|
| Critical | Live credential in plain text (API key in code, key in a `.txt`, key pasted into shell history), private key or certificate in a synced folder, password spreadsheet | Rotate or revoke first, then remove the file; move keys to a password manager or secret store |
| High | `.env` or OAuth token files inside a cloud-synced folder (`.gitignore` does not stop sync); `.env.example` that once received a real key; wildcard permissions in Claude Code settings that allow arbitrary command execution; build files that publish internal folders | Move out of the synced folder; add a pre-commit check for key patterns; narrow the permissions; fix the build before the next deploy |
| Medium | Internal hostnames, IPs or usernames in notes; personal email addresses in published pages; sensitive memories syncing to a work machine | Replace with generic references; verify public URLs; reduce the memory to the rule |

Each entry: level, what (without the value), where (path in backticks),
action, and "to confirm" when the inventory could not verify it. Nothing in
`SEGURANCA.md` is fixed by the setup: every action belongs to the user.

## The panel (Nexaya OS Pro)

Only when the Pro is installed; details in `painel.md`.

- Binds to `127.0.0.1` only, checks the `Host` header, requires a per-session
  token for its API and a local `Origin` for actions, and serves its page with a
  strict Content-Security-Policy. Generated HTML is previewed in a sandbox.
- It refuses sensitive-looking file names and `memorias_privadas`.
- **`apps.json` is a root of trust.** The panel starts only what is registered
  there, with a closed list of executables and no shell metacharacters, but
  whoever edits `apps.json` decides what can run. The OS folder must not be
  shared or writable by others.
- Never bind it to `0.0.0.0`. The only way to reach it from another device
  is `tailscale serve`, inside the user's own tailnet. Never `tailscale
  funnel`, never another tunnel, reverse proxy or port forward.

## Global changes need a yes

Ask before each of these, showing the exact change:

- writing or appending to `~/.claude/CLAUDE.md`;
- editing `~/.claude/settings.json` (for example `autoMemoryDirectory`);
- creating a scheduled task or a scheduler entry;
- creating junctions or symlinks in `~/.claude/skills/`;
- adding an entry to any `launch.json`.

## Final privacy checklist (step 7)

- [ ] `grep` the new OS files for key patterns (`sk-`, `sk_`, `AIza`, `ghp_`,
      `gho_`, `xox`, `-----BEGIN`, `password=`, `token=`): no hits.
- [ ] No link in any router points to a file matching the "never open" list.
- [ ] `SEGURANCA.md` has paths and actions only, no values.
- [ ] No health, financial or third-party personal data in routers or memory.
- [ ] With the Pro installed: memories listed as private are in
      `memorias_privadas` of the panel config.
- [ ] No `0.0.0.0` in the panel config (Pro), and `apps.json` only has commands the
      user recognizes.
