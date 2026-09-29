"""Práctica : lectura de píxeles de un archivo BMP de 24 bits.
"""
import sys

RUTA_POR_DEFECTO = "C:\Users\anton\OneDrive\Imágenes\Capturas de pantalla\Captura de pantalla 2026-09-28 122841.pngimagen.bmp"


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else RUTA_POR_DEFECTO

    with open(ruta, "rb") as file:
        firma = file.read(2)              # debe ser b'BM'
        print("Firma:", firma)
        if firma != b"BM":
            raise SystemExit("El archivo no es un BMP válido.")

        file.seek(54, 0)                 
        primer_pixel = file.read(3)       
        print("Primer píxel (BGR):", primer_pixel)

        file.seek(54, 0)
        no_pix = 0
        while True:
            pixel_data = file.read(3)
            if len(pixel_data) > 0:
                print(pixel_data)
                no_pix += 1
            else:
                break

    print("No Pixels: " + str(no_pix))


if __name__ == "__main__":
    main()
