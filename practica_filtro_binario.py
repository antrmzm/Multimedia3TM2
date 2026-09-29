"""Práctica 4: filtro binario (blanco y negro) sobre un BMP de 24 bits.

Genera dos archivos: la versión binaria y la versión invertida.

Uso:
    python practica04_filtro_binario.py images/imagen.bmp
"""
import sys

RUTA_POR_DEFECTO = "./images/imagen.bmp"
BLANCO = [0xFF, 0xFF, 0xFF]
NEGRO = [0x00, 0x00, 0x00]


def aplicar_filtro(ruta_entrada, ruta_salida, invertir=False):
    """Escribe una copia binarizada de la imagen. Devuelve el no. de píxeles."""
    oscuro, claro = (BLANCO, NEGRO) if invertir else (NEGRO, BLANCO)
    limite = (pow(2, 24) - 1) / 2         # mitad del rango de 24 bits

    with open(ruta_entrada, "rb") as file, open(ruta_salida, "wb") as fileo:
        metadata = file.read(54)          # copiar header (54 bytes)
        fileo.write(metadata)

        file.seek(54, 0)
        no_pix = 0
        while True:
            pixel_data = file.read(3)
            if len(pixel_data) > 0:
                valor_int = int.from_bytes(bytes(pixel_data), byteorder="little")
                if valor_int < limite:
                    fileo.write(bytes(oscuro))
                else:
                    fileo.write(bytes(claro))
                no_pix += 1
            else:
                break
    return no_pix


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else RUTA_POR_DEFECTO
    base = ruta[:-4] if ruta.lower().endswith(".bmp") else ruta

    n = aplicar_filtro(ruta, base + "_binario.bmp")
    print("Filtro binario listo. No Pixels: " + str(n))
    n = aplicar_filtro(ruta, base + "_binario_invertido.bmp", invertir=True)
    print("Filtro invertido listo. No Pixels: " + str(n))


if __name__ == "__main__":
    main()
