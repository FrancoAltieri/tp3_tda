from coloreo_inicial import colorear_por_mayoria
from estado_busqueda import EstadoBusqueda
from solucion import Solucion
from tablero import SIN_COLOR


class BuscadorBacktracking:
    def __init__(self, tablero):
        self.tablero = tablero
        self.estado = EstadoBusqueda(tablero)
        self.mejor_coloreo = colorear_por_mayoria(tablero)
        self.mejor_cantidad_filas_vacias = Solucion(tablero, self.mejor_coloreo).cantidad_filas_vacias()
        self.nodos_explorados = 0

    def resolver(self):
        self.explorar()
        return Solucion(self.tablero, self.mejor_coloreo)

    def explorar(self):
        self.nodos_explorados += 1
        if self.estado.esta_resuelto():
            self.registrar_candidata()
            return
        if self.estado.cota_inferior_filas_vacias() >= self.mejor_cantidad_filas_vacias:
            return
        columna, color = self.estado.buscar_asignacion_dominante()
        if columna != SIN_COLOR:
            self.estado.asignar(columna, color)
            self.explorar()
            self.estado.desasignar(columna, color)
            return
        columna = self.estado.elegir_columna()
        for color in self.estado.colores_en_orden_de_prueba(columna):
            self.estado.asignar(columna, color)
            self.explorar()
            self.estado.desasignar(columna, color)

    def registrar_candidata(self):
        if self.estado.filas_vacias < self.mejor_cantidad_filas_vacias:
            self.mejor_cantidad_filas_vacias = self.estado.filas_vacias
            self.mejor_coloreo = self.completar_columnas_libres()

    def completar_columnas_libres(self):
        coloreo = list(self.estado.color_por_columna)
        mayoritarios = colorear_por_mayoria(self.tablero)
        for columna in self.estado.columnas_libres:
            coloreo[columna] = mayoritarios[columna]
        return coloreo
