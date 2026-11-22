from pathlib import Path
import sys
import time

from buscador_backtracking import BuscadorBacktracking
from lector_tablero import leer_tablero

CARPETA_POR_DEFECTO = Path("set_datos_alumnos")


def medir_archivo(ruta: Path):
    tablero = leer_tablero(ruta)
    inicio = time.perf_counter()
    buscador = BuscadorBacktracking(tablero)
    solucion = buscador.resolver()
    duracion = time.perf_counter() - inicio
    return tablero, solucion, buscador.nodos_explorados, duracion


def imprimir_medicion(ruta: Path):
    tablero, solucion, nodos, duracion = medir_archivo(ruta)
    dimension = f"{tablero.cantidad_filas}x{tablero.cantidad_columnas}"
    print(
        f"{ruta}: {dimension} filas_vacias={solucion.cantidad_filas_vacias()} "
        f"nodos={nodos} tiempo={duracion:.2f}s",
        flush=True,
    )


def obtener_archivos(argumentos: list[str]) -> list[Path]:
    if len(argumentos) > 1:
        return [Path(arg) for arg in argumentos[1:]]

    if not CARPETA_POR_DEFECTO.is_dir():
        raise FileNotFoundError(f"No se encontró la carpeta '{CARPETA_POR_DEFECTO}'")

    return sorted(CARPETA_POR_DEFECTO.glob("*.txt"))


def main(argumentos: list[str]) -> int:
    archivos = obtener_archivos(argumentos)
    if not archivos:
        print(f"No se encontraron archivos .txt en '{CARPETA_POR_DEFECTO}'", file=sys.stderr)
        return 1

    for ruta in archivos:
        imprimir_medicion(ruta)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
