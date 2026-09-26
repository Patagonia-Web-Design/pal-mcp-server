# Fork de AIKen — PAL MCP como puente a los ayudantes

Rama `aiken` (default del fork). Upstream: `BeehiveInnovations/pal-mcp-server`, sin commits
desde el 15/12/2025 (v9.8.2).

## Qué cambia respecto de upstream

- Merge de los PR #482 (pin `mcp<2`, `black`) y #481 (clientes de clink por config + `agy`),
  sin mergear en upstream.
- `clink` ofrece solo tres clientes, **todos en solo lectura**:

| Cliente | CLI | Para qué | Solo lectura por |
|---|---|---|---|
| `agy` | Antigravity (Gemini, plan AI Pro) | lectura pesada, síntesis, segunda opinión | `--mode plan` + prompts de rol |
| `codex` | Codex CLI (ChatGPT) | revisar un diff — el cupo es chico | `--sandbox read-only` |
| `nlm` | NotebookLM, notebook "AIKen KB" | preguntas sobre el vault | es una consulta, no ejecuta nada |

- Se quitaron `gemini` (Gemini CLI fue reemplazada por Antigravity para Google One el
  18/06/2026) y `claude` (Claude Code se llamaría a sí mismo).
- Los tests exigen solo lectura: con los flags de bypass de upstream, fallan.

## Cómo corre

Registrado a nivel usuario en Claude Code:

```
claude mcp add --scope user pal \
  -e DISABLED_TOOLS=chat,thinkdeep,planner,consensus,codereview,precommit,debug,secaudit,docgen,analyze,refactor,tracer,testgen,challenge,apilookup \
  -e LOG_LEVEL=WARNING \
  -- /Volumes/T7Shield/pal-mcp-server/.venv/bin/python /Volumes/T7Shield/pal-mcp-server/server.py
```

Expone `clink`, `listmodels` y `version` (~500 tokens de definición). Sin API keys.
**Depende de que el T7 esté montado**: si no está, el MCP `pal` no conecta y nada más se rompe.

Quitar: `claude mcp remove pal -s user`.

## Actualizar desde upstream

```
git fetch upstream && git merge upstream/main   # merge, nunca rebase
.venv/bin/python -m pytest -q tests -m "not integration"
git push origin aiken
```

## Cómo se usa desde AIKen

Skill `meta/consultar-ayudante` en `aiken-agent-os`: cuándo delegar a cuál y cómo verificar
lo que devuelve (NotebookLM puede citar mal).
