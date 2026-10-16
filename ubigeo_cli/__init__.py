"""Busqueda y validacion de ubigeos del INEI (departamento, provincia, distrito)."""
import csv
import re
import unicodedata
from functools import lru_cache
from importlib import resources

__version__ = "0.1.0"
FUENTE = "INEI, Codigos de ubicacion geografica (1,891 distritos, version 2022)"


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s).strip().upper()


@lru_cache(maxsize=1)
def _filas() -> tuple:
    with resources.files("ubigeo_cli").joinpath("ubigeo_inei_2022.csv").open("r", encoding="utf-8", newline="") as f:
        filas = []
        for r in csv.DictReader(f):
            r["_texto"] = _norm(f'{r["distrito"]} {r["provincia"]} {r["departamento"]}')
            filas.append(r)
    return tuple(filas)


def _publico(r: dict) -> dict:
    return {k: v for k, v in r.items() if not k.startswith("_")}


def validar(codigo: str) -> dict:
    """Valida un codigo de 2 (departamento), 4 (provincia) o 6 (distrito) digitos."""
    c = (codigo or "").strip()
    if not re.fullmatch(r"\d{2}|\d{4}|\d{6}", c):
        return {"valido": False, "codigo": c, "motivo": "Debe tener 2, 4 o 6 digitos numericos"}
    nivel = {2: "departamento", 4: "provincia", 6: "distrito"}[len(c)]
    for r in _filas():
        if r["ubigeo"].startswith(c):
            return {"valido": True, "codigo": c, "nivel": nivel}
    return {"valido": False, "codigo": c, "motivo": f"No existe ese {nivel} en la version 2022 del INEI"}


def info(codigo: str):
    """Datos de un distrito (6 digitos), o resumen de departamento/provincia (2/4 digitos). None si no es valido."""
    c = (codigo or "").strip()
    v = validar(c)
    if not v["valido"]:
        return None
    coinc = [r for r in _filas() if r["ubigeo"].startswith(c)]
    if len(c) == 6:
        return _publico(coinc[0])
    base = {"ubigeo": c, "nivel": v["nivel"], "departamento": coinc[0]["departamento"], "distritos": len(coinc)}
    if len(c) == 4:
        base["provincia"] = coinc[0]["provincia"]
    else:
        base["provincias"] = len({r["ubigeo"][:4] for r in coinc})
    return base


def buscar(texto: str, limite: int = 20) -> list:
    """Todas las palabras deben aparecer (sin importar tildes ni mayusculas) en distrito/provincia/departamento."""
    palabras = _norm(texto).split()
    if not palabras:
        return []
    clave = _norm(texto)
    out = [r for r in _filas() if all(p in r["_texto"] for p in palabras)]
    out.sort(key=lambda r: (0 if _norm(r["distrito"]) == clave else 1 if clave in _norm(r["distrito"]) else 2, r["ubigeo"]))
    return [_publico(r) for r in out[:limite]]


def listar(departamento: str, provincia=None) -> list:
    d = _norm(departamento)
    out = [r for r in _filas() if _norm(r["departamento"]) == d]
    if provincia:
        p = _norm(provincia)
        out = [r for r in out if _norm(r["provincia"]) == p]
    return [_publico(r) for r in out]
