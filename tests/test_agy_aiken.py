"""bin/agy-aiken: qué niega dentro de una carpeta permitida a Gemini."""

import importlib.machinery
import importlib.util
from pathlib import Path

RUTA = Path(__file__).resolve().parent.parent / "bin" / "agy-aiken"


def cargar():
    cargador = importlib.machinery.SourceFileLoader("agy_aiken", str(RUTA))
    spec = importlib.util.spec_from_loader("agy_aiken", cargador)
    modulo = importlib.util.module_from_spec(spec)
    cargador.exec_module(modulo)
    return modulo


def test_niega_secretos_y_clientes_y_deja_el_resto(tmp_path):
    for rel in [".env.local", ".envrc", "w/.dev.vars", "k.pem", "h/.wwebjs_auth/s",
                "docs/d1-backups/x.json", "vault/clients/a.md", "ref/clientes/b.md",
                ".env.example", "skills/x.md", "node_modules/p/.env"]:
        archivo = tmp_path / rel
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_text("x")

    negadas = {str(p.relative_to(tmp_path)) for p in cargar().sensibles(tmp_path)}

    assert negadas == {".env.local", ".envrc", "w/.dev.vars", "k.pem", "h/.wwebjs_auth",
                       "docs/d1-backups", "vault/clients", "ref/clientes"}
