import sys

from buscador_backtracking import BuscadorBacktracking
from lector_tablero import leer_tablero, TableroInvalido
from presentacion import formatear_solucion

CODIGO_USO_INCORRECTO = 2
CODIGO_ARCHIVO_INVALIDO = 1


def resolver_tablero(tablero):
    return BuscadorBacktracking(tablero).resolver()


def main(argumentos):
    if len(argumentos) != 2:
        print("Uso: python3 tp3.py ruta/a/tablero.txt", file=sys.stderr)
        return CODIGO_USO_INCORRECTO
    try:
        tablero = leer_tablero(argumentos[1])
    except (OSError, TableroInvalido) as error:
        print(f"No se pudo leer el tablero: {error}", file=sys.stderr)
        return CODIGO_ARCHIVO_INVALIDO
    print(formatear_solucion(resolver_tablero(tablero)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
