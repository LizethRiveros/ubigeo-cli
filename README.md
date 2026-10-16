# ubigeo-cli

Busca y valida **ubigeos del INEI** (departamento, provincia, distrito) del Perú, desde la terminal o desde Python.
Sin dependencias, funciona sin internet: los 1,891 distritos vienen incluidos.

```console
$ ubigeo buscar ayacucho huanta
050401  HUANTA · HUANTA · AYACUCHO
050402  AYAHUANCO · HUANTA · AYACUCHO

$ ubigeo info 090101
090101  HUANCAVELICA · HUANCAVELICA · HUANCAVELICA
Capital: HUANCAVELICA · Region natural: SIERRA

$ ubigeo validar 999999      # exit 1 si no existe
no valido: No existe ese distrito en la version 2022 del INEI

$ ubigeo --json listar huancavelica tayacaja
```

La búsqueda ignora tildes y mayúsculas, y todas las palabras deben aparecer en distrito, provincia o departamento.

## Instalar

```bash
pip install .          # desde esta carpeta; instala el comando `ubigeo`
python -m ubigeo_cli buscar lima    # sin instalar
```

Desde Python:

```python
from ubigeo_cli import buscar, info, validar, listar
info("090101")["distrito"]     # 'HUANCAVELICA'
validar("0901")["nivel"]       # 'provincia'
```

## Pruebas

```bash
python -m unittest discover -s tests -t .
```

## Alcance y límites

- **Fuente:** INEI, *Código de ubicación geográfica en el Perú*, versión 2022 (1,891 distritos), publicada en datosabiertos.gob.pe. Proyecto no oficial.
- **Solo códigos INEI.** RENIEC, SUNAT y otras instituciones usan sus propios códigos o variantes. La conversión entre instituciones (`convertir`) **no está implementada**: requiere sus tablas de equivalencia oficiales, que aún no se han verificado.
- Los distritos creados o modificados después de la versión 2022 no aparecen hasta actualizar el CSV (`ubigeo_cli/ubigeo_inei_2022.csv`).
