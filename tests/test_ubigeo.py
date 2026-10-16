import unittest

from ubigeo_cli import buscar, info, listar, validar


class Ubigeo(unittest.TestCase):
    def test_validar(self):
        self.assertTrue(validar("090101")["valido"])
        self.assertEqual(validar("09")["nivel"], "departamento")
        self.assertEqual(validar("0901")["nivel"], "provincia")
        self.assertFalse(validar("999999")["valido"])
        self.assertFalse(validar("9101")["valido"])
        self.assertFalse(validar("abc123")["valido"])
        self.assertFalse(validar("")["valido"])

    def test_info_distrito(self):
        r = info("090101")
        self.assertEqual(r["departamento"], "HUANCAVELICA")
        self.assertEqual(r["distrito"], "HUANCAVELICA")

    def test_info_niveles(self):
        self.assertEqual(info("09")["departamento"], "HUANCAVELICA")
        self.assertEqual(info("09")["provincias"], 7)
        self.assertEqual(info("0901")["provincia"], "HUANCAVELICA")
        self.assertIsNone(info("99"))

    def test_buscar_sin_tildes_y_orden(self):
        r = buscar("huancavelica")
        self.assertTrue(r)
        self.assertEqual(r[0]["ubigeo"], "090101")
        self.assertEqual(buscar("ASUNCIÓN chachapoyas")[0]["ubigeo"], "010102")
        self.assertEqual(buscar("zzzzxx"), [])
        self.assertEqual(buscar("   "), [])

    def test_listar_provincia(self):
        r = listar("huancavelica", "Tayacaja")
        self.assertTrue(all(x["provincia"] == "TAYACAJA" for x in r))
        self.assertGreater(len(r), 5)

    def test_totales_nacionales(self):
        from ubigeo_cli import _filas
        filas = _filas()
        self.assertEqual(len(filas), 1891)
        self.assertEqual(len({f["ubigeo"] for f in filas}), 1891)
        self.assertEqual(len({f["ubigeo"][:2] for f in filas}), 25)


if __name__ == "__main__":
    unittest.main()
