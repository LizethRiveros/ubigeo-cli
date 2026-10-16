import argparse
import json
import sys

from . import __version__, buscar, info, listar, validar


def _linea(r: dict) -> str:
    return f'{r["ubigeo"]}  {r["distrito"]} · {r["provincia"]} · {r["departamento"]}'


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="ubigeo", description="Busca y valida ubigeos del INEI (Peru).")
    ap.add_argument("--json", action="store_true", help="salida en JSON")
    ap.add_argument("--version", action="version", version=f"ubigeo-cli {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("buscar", help="buscar por nombre de distrito, provincia o departamento")
    b.add_argument("texto", nargs="+")
    b.add_argument("-n", "--limite", type=int, default=20)
    i = sub.add_parser("info", help="datos de un codigo de 2, 4 o 6 digitos")
    i.add_argument("codigo")
    v = sub.add_parser("validar", help="valida un codigo (exit 0 si es valido)")
    v.add_argument("codigo")
    li = sub.add_parser("listar", help="distritos de un departamento (y provincia)")
    li.add_argument("departamento")
    li.add_argument("provincia", nargs="?")
    a = ap.parse_args(argv)

    if a.cmd == "buscar":
        res = buscar(" ".join(a.texto), a.limite)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print("\n".join(_linea(r) for r in res) or "Sin resultados.")
        return 0 if res else 1
    if a.cmd == "info":
        r = info(a.codigo)
        if r is None:
            print(json.dumps(validar(a.codigo), ensure_ascii=False) if a.json else f"Codigo no valido: {a.codigo}")
            return 1
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        elif "distrito" in r:
            print(_linea(r))
            print(f'Capital: {r["capital"]} · Region natural: {r["region_natural"]}')
        else:
            print(json.dumps(r, ensure_ascii=False))
        return 0
    if a.cmd == "validar":
        r = validar(a.codigo)
        print(json.dumps(r, ensure_ascii=False) if a.json else ("valido" if r["valido"] else "no valido: " + r["motivo"]))
        return 0 if r["valido"] else 1
    if a.cmd == "listar":
        res = listar(a.departamento, a.provincia)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print("\n".join(_linea(r) for r in res) or "Sin resultados.")
        return 0 if res else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
