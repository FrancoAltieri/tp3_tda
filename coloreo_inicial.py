from tablero import COLOR_VERDE, COLOR_CELESTE, SIN_COLOR


def color_mayoritario(tablero, columna):
    verdes = tablero.cantidad_piedras_de_columna(columna, COLOR_VERDE)
    celestes = tablero.cantidad_piedras_de_columna(columna, COLOR_CELESTE)
    if verdes == 0 and celestes == 0:
        return SIN_COLOR
    if verdes >= celestes:
        return COLOR_VERDE
    return COLOR_CELESTE


def colorear_por_mayoria(tablero):
    return [color_mayoritario(tablero, columna) for columna in range(tablero.cantidad_columnas)]
