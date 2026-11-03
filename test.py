import os
import unittest
 
from buscador_backtracking import BuscadorBacktracking
from lector_resultados_esperados import leer_resultados_esperados
from lector_tablero import leer_tablero
 
DIRECTORIO_CASOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "set_datos_catedra")
ARCHIVO_RESULTADOS_ESPERADOS = os.path.join(DIRECTORIO_CASOS, "Resultados Esperados.txt")
 
 
class PruebaDeArchivo(unittest.TestCase):
    def __init__(self, resultado_esperado):
        super().__init__("test_filas_vacias_coinciden_con_las_esperadas")
        self.resultado_esperado = resultado_esperado
 
    def __str__(self):
        return self.resultado_esperado.nombre_archivo
 
    def test_filas_vacias_coinciden_con_las_esperadas(self):
        ruta = os.path.join(DIRECTORIO_CASOS, self.resultado_esperado.nombre_archivo)
        solucion = BuscadorBacktracking(leer_tablero(ruta)).resolver()
        self.assertEqual(self.resultado_esperado.cantidad_filas_vacias, solucion.cantidad_filas_vacias())
 
 
def load_tests(loader, tests, pattern):
    resultados = leer_resultados_esperados(ARCHIVO_RESULTADOS_ESPERADOS)
    return unittest.TestSuite(PruebaDeArchivo(resultado) for resultado in resultados.values())
 
 
if __name__ == "__main__":
    unittest.main(verbosity=2)