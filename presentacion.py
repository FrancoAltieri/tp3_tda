SEPARADOR_COLUMNAS = " "
SEPARADOR_PIEDRAS = ", "
SIN_PIEDRAS_REMOVIDAS = "-"


def formatear_colores(solucion):
    simbolos = [solucion.simbolo_de_columna(columna) for columna in range(solucion.tablero.cantidad_columnas)]
    return SEPARADOR_COLUMNAS.join(simbolos)


def formatear_piedras_removidas(solucion):
    if not solucion.piedras_removidas:
        return SIN_PIEDRAS_REMOVIDAS
    return SEPARADOR_PIEDRAS.join(f"({fila}, {columna})" for fila, columna in solucion.piedras_removidas)


def formatear_filas_vacias(solucion):
    if not solucion.filas_vacias:
        return "0"
    return f"{solucion.cantidad_filas_vacias()} -> {solucion.filas_vacias}"


def formatear_solucion(solucion):
    lineas = [
        f"Colores por columna: {formatear_colores(solucion)}",
        f"Piedras removidas: {formatear_piedras_removidas(solucion)}",
        "Tablero resultante:",
        *solucion.tablero_resultante(),
        f"Filas vacías: {formatear_filas_vacias(solucion)}",
    ]
    return "\n".join(lineas)
