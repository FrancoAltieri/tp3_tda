from tablero import Tablero, VACIO, VERDE, CELESTE

PREFIJO_COMENTARIO = "#"
SIMBOLOS_VALIDOS = {VACIO, VERDE, CELESTE}


class TableroInvalido(Exception):
    pass


def es_linea_de_tablero(linea):
    return linea != "" and not linea.startswith(PREFIJO_COMENTARIO)


def leer_lineas(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        lineas = [linea.strip() for linea in archivo]
    return [linea for linea in lineas if es_linea_de_tablero(linea)]


def validar_filas(filas):
    if not filas:
        raise TableroInvalido("El archivo no contiene ninguna fila de tablero")
    ancho = len(filas[0])
    for numero, fila in enumerate(filas):
        if len(fila) != ancho:
            raise TableroInvalido(f"La fila {numero} tiene {len(fila)} columnas y se esperaban {ancho}")
        if not set(fila) <= SIMBOLOS_VALIDOS:
            raise TableroInvalido(f"La fila {numero} contiene símbolos inválidos")


def leer_tablero(ruta):
    filas = leer_lineas(ruta)
    validar_filas(filas)
    return Tablero(filas)
