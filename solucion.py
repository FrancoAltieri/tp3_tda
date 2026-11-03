from tablero import COLOR_VERDE, COLOR_CELESTE, SIN_COLOR, SIMBOLO_POR_COLOR, VACIO

SIMBOLO_SIN_COLOR = "-"


class Solucion:
    def __init__(self, tablero, colores_por_columna):
        self.tablero = tablero
        self.colores_por_columna = colores_por_columna
        self.piedras_removidas = self.calcular_piedras_removidas()
        self.filas_vacias = self.calcular_filas_vacias()

    def conserva_piedra(self, fila, columna):
        if not self.tablero.hay_piedra(fila, columna):
            return False
        return self.tablero.color_de_piedra(fila, columna) == self.colores_por_columna[columna]

    def calcular_piedras_removidas(self):
        removidas = []
        for fila in range(self.tablero.cantidad_filas):
            for columna in range(self.tablero.cantidad_columnas):
                if self.tablero.hay_piedra(fila, columna) and not self.conserva_piedra(fila, columna):
                    removidas.append((fila, columna))
        return removidas

    def calcular_filas_vacias(self):
        vacias = []
        for fila in range(self.tablero.cantidad_filas):
            if not self.fila_conserva_alguna_piedra(fila):
                vacias.append(fila)
        return vacias

    def fila_conserva_alguna_piedra(self, fila):
        for columna in range(self.tablero.cantidad_columnas):
            if self.conserva_piedra(fila, columna):
                return True
        return False

    def cantidad_filas_vacias(self):
        return len(self.filas_vacias)

    def simbolo_de_columna(self, columna):
        color = self.colores_por_columna[columna]
        if color == SIN_COLOR:
            return SIMBOLO_SIN_COLOR
        return SIMBOLO_POR_COLOR[color]

    def simbolo_de_celda(self, fila, columna):
        if self.conserva_piedra(fila, columna):
            return SIMBOLO_POR_COLOR[self.colores_por_columna[columna]]
        return VACIO

    def tablero_resultante(self):
        filas = []
        for fila in range(self.tablero.cantidad_filas):
            simbolos = [self.simbolo_de_celda(fila, columna) for columna in range(self.tablero.cantidad_columnas)]
            filas.append("".join(simbolos))
        return filas

    def es_valida(self):
        for columna in range(self.tablero.cantidad_columnas):
            if self.columna_mezcla_colores(columna):
                return False
        return True

    def columna_mezcla_colores(self, columna):
        colores = set()
        for fila in range(self.tablero.cantidad_filas):
            if self.conserva_piedra(fila, columna):
                colores.add(self.tablero.color_de_piedra(fila, columna))
        return len(colores) > 1
