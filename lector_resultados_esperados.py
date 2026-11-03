import re
from dataclasses import dataclass

PATRON_ENCABEZADO_DE_BLOQUE = re.compile(r"^\S+\.txt$")
PATRON_FILAS_VACIAS = re.compile(r"^Filas vacías: (\d+)")


class ResultadosEsperadosInvalidos(Exception):
    pass


@dataclass(frozen=True)
class ResultadoEsperado:
    nombre_archivo: str
    cantidad_filas_vacias: int


def es_encabezado_de_bloque(linea):
    return PATRON_ENCABEZADO_DE_BLOQUE.match(linea) is not None


def dividir_en_bloques(lineas):
    bloques = {}
    nombre_actual = None
    for linea in lineas:
        if es_encabezado_de_bloque(linea):
            nombre_actual = linea
            bloques[nombre_actual] = []
        elif nombre_actual is not None:
            bloques[nombre_actual].append(linea)
    return bloques


def extraer_cantidad_filas_vacias(lineas):
    for linea in lineas:
        coincidencia = PATRON_FILAS_VACIAS.match(linea)
        if coincidencia:
            return int(coincidencia.group(1))
    raise ResultadosEsperadosInvalidos("No se encontró la línea 'Filas vacías'")


def construir_resultado(nombre_archivo, lineas):
    try:
        cantidad = extraer_cantidad_filas_vacias(lineas)
    except ResultadosEsperadosInvalidos as error:
        raise ResultadosEsperadosInvalidos(f"{nombre_archivo}: {error}") from error
    return ResultadoEsperado(nombre_archivo, cantidad)


def leer_resultados_esperados(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        lineas = [linea.rstrip("\n") for linea in archivo]
    bloques = dividir_en_bloques(lineas)
    return {nombre: construir_resultado(nombre, bloque) for nombre, bloque in bloques.items()}
