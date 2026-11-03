from tablero import COLOR_VERDE, COLOR_CELESTE, SIN_COLOR


class EstadoBusqueda:
    def __init__(self, tablero):
        self.cantidad_filas = tablero.cantidad_filas
        self.cantidad_columnas = tablero.cantidad_columnas
        self.piedras_por_fila = self.indexar_piedras_por_fila(tablero)
        self.filas_por_columna = self.indexar_filas_por_columna(tablero)
        self.color_por_columna = [SIN_COLOR] * self.cantidad_columnas
        self.columnas_libres = set(range(self.cantidad_columnas))
        self.satisfacciones_por_fila = [0] * self.cantidad_filas
        self.pendientes_por_fila = [len(piedras) for piedras in self.piedras_por_fila]
        self.unitarias = [[0] * self.cantidad_columnas, [0] * self.cantidad_columnas]
        self.abiertas_por_columna = [[0] * self.cantidad_columnas, [0] * self.cantidad_columnas]
        self.filas_vacias = 0
        self.filas_abiertas = 0
        self.inicializar_contadores()

    def indexar_piedras_por_fila(self,tablero):
        return [tablero.piedras_de_fila(fila) for fila in range(tablero.cantidad_filas)]

    def indexar_filas_por_columna(self,tablero):
        filas_por_columna = [
            [[] for _ in range(tablero.cantidad_columnas)],
            [[] for _ in range(tablero.cantidad_columnas)],
        ]
        for fila in range(tablero.cantidad_filas):
            for columna, color in tablero.piedras_de_fila(fila):
                filas_por_columna[color][columna].append(fila)
        return filas_por_columna

    def inicializar_contadores(self):
        for fila in range(self.cantidad_filas):
            pendientes = self.pendientes_por_fila[fila]
            if pendientes == 0:
                self.filas_vacias += 1
                continue
            self.filas_abiertas += 1
            for columna, color in self.piedras_por_fila[fila]:
                self.abiertas_por_columna[color][columna] += 1
            if pendientes == 1:
                columna, color = self.piedras_por_fila[fila][0]
                self.unitarias[color][columna] += 1

    def esta_resuelto(self):
        return self.filas_abiertas == 0

    def cantidad_filas_de_columna(self, columna, color):
        return len(self.filas_por_columna[color][columna])

    def columna_pendiente_de_fila(self, fila, columna_excluida=SIN_COLOR):
        for columna, color in self.piedras_por_fila[fila]:
            if self.color_por_columna[columna] == SIN_COLOR and columna != columna_excluida:
                return columna, color
        return SIN_COLOR, SIN_COLOR

    def asignar(self, columna, color):
        self.color_por_columna[columna] = color
        self.columnas_libres.discard(columna)
        self.satisfacer_filas(columna, color)
        self.debilitar_filas(columna, 1 - color)

    def satisfacer_filas(self, columna, color):
        for fila in self.filas_por_columna[color][columna]:
            if self.satisfacciones_por_fila[fila] == 0:
                self.filas_abiertas -= 1
                self.retirar_fila_de_columnas_libres(fila)
                if self.pendientes_por_fila[fila] == 1:
                    self.unitarias[color][columna] -= 1
            self.satisfacciones_por_fila[fila] += 1
            self.pendientes_por_fila[fila] -= 1

    def debilitar_filas(self, columna, color_descartado):
        for fila in self.filas_por_columna[color_descartado][columna]:
            self.pendientes_por_fila[fila] -= 1
            if self.satisfacciones_por_fila[fila] > 0:
                continue
            if self.pendientes_por_fila[fila] == 0:
                self.filas_vacias += 1
                self.filas_abiertas -= 1
                self.unitarias[color_descartado][columna] -= 1
            elif self.pendientes_por_fila[fila] == 1:
                columna_unica, color_unico = self.columna_pendiente_de_fila(fila)
                self.unitarias[color_unico][columna_unica] += 1

    def desasignar(self, columna, color):
        self.restaurar_filas_debilitadas(columna, 1 - color)
        self.restaurar_filas_satisfechas(columna, color)
        self.color_por_columna[columna] = SIN_COLOR
        self.columnas_libres.add(columna)

    def restaurar_filas_debilitadas(self, columna, color_descartado):
        for fila in self.filas_por_columna[color_descartado][columna]:
            if self.satisfacciones_por_fila[fila] == 0:
                if self.pendientes_por_fila[fila] == 1:
                    columna_unica, color_unico = self.columna_pendiente_de_fila(fila, columna)
                    self.unitarias[color_unico][columna_unica] -= 1
                elif self.pendientes_por_fila[fila] == 0:
                    self.filas_vacias -= 1
                    self.filas_abiertas += 1
                    self.unitarias[color_descartado][columna] += 1
            self.pendientes_por_fila[fila] += 1

    def restaurar_filas_satisfechas(self, columna, color):
        for fila in self.filas_por_columna[color][columna]:
            self.satisfacciones_por_fila[fila] -= 1
            self.pendientes_por_fila[fila] += 1
            if self.satisfacciones_por_fila[fila] == 0:
                self.filas_abiertas += 1
                self.reponer_fila_en_columnas_libres(fila)
                if self.pendientes_por_fila[fila] == 1:
                    self.unitarias[color][columna] += 1

    def retirar_fila_de_columnas_libres(self, fila):
        for columna, color in self.piedras_por_fila[fila]:
            if self.color_por_columna[columna] == SIN_COLOR:
                self.abiertas_por_columna[color][columna] -= 1

    def reponer_fila_en_columnas_libres(self, fila):
        for columna, color in self.piedras_por_fila[fila]:
            if self.color_por_columna[columna] == SIN_COLOR:
                self.abiertas_por_columna[color][columna] += 1

    def buscar_asignacion_dominante(self):
        for columna in self.columnas_libres:
            for color in (COLOR_VERDE, COLOR_CELESTE):
                if self.unitarias[color][columna] >= self.abiertas_por_columna[1 - color][columna]:
                    return columna, color
        return SIN_COLOR, SIN_COLOR

    def cota_inferior_filas_vacias(self):
        cota = self.filas_vacias
        for columna in self.columnas_libres:
            cota += min(self.unitarias[COLOR_VERDE][columna], self.unitarias[COLOR_CELESTE][columna])
        return cota

    def prioridad_de_columna(self, columna):
        verdes = self.unitarias[COLOR_VERDE][columna]
        celestes = self.unitarias[COLOR_CELESTE][columna]
        abiertas = self.abiertas_por_columna[COLOR_VERDE][columna] + self.abiertas_por_columna[COLOR_CELESTE][columna]
        return (verdes * celestes, verdes + celestes, abiertas)

    def elegir_columna(self):
        return max(self.columnas_libres, key=self.prioridad_de_columna)

    def colores_en_orden_de_prueba(self, columna):
        verdes = self.cantidad_filas_de_columna(columna, COLOR_VERDE)
        celestes = self.cantidad_filas_de_columna(columna, COLOR_CELESTE)
        if verdes >= celestes:
            return (COLOR_VERDE, COLOR_CELESTE)
        return (COLOR_CELESTE, COLOR_VERDE)
