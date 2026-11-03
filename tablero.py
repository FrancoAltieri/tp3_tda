VACIO = "."
VERDE = "V"
CELESTE = "C"

COLOR_VERDE = 0
COLOR_CELESTE = 1
SIN_COLOR = -1

SIMBOLO_POR_COLOR = {COLOR_VERDE: VERDE, COLOR_CELESTE: CELESTE}
COLOR_POR_SIMBOLO = {VERDE: COLOR_VERDE, CELESTE: COLOR_CELESTE}


class Tablero:
    def __init__(self, filas):
        self.filas = filas
        self.cantidad_filas = len(filas)
        self.cantidad_columnas = len(filas[0]) if filas else 0

    def hay_piedra(self, fila, columna):
        return self.filas[fila][columna] != VACIO

    def color_de_piedra(self, fila, columna):
        return COLOR_POR_SIMBOLO[self.filas[fila][columna]]

    def piedras_de_fila(self, fila):
        piedras = []
        for columna in range(self.cantidad_columnas):
            if self.hay_piedra(fila, columna):
                piedras.append((columna, self.color_de_piedra(fila, columna)))
        return piedras

    def cantidad_piedras_de_columna(self, columna, color):
        cantidad = 0
        for fila in range(self.cantidad_filas):
            if self.hay_piedra(fila, columna) and self.color_de_piedra(fila, columna) == color:
                cantidad += 1
        return cantidad
