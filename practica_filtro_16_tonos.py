"""Práctica 5: filtro de 16 tonos con una paleta de un color base.

Edita PALETA_HEX con tus 16 colores (del más oscuro al más claro).
Ejemplo incluido: escala de azules.

Uso:
    python practica05_filtro_16_tonos.py images/imagen.bmp
"""
import sys

RUTA_POR_DEFECTO = "./images/imagen.bmp"

# 16 tonos en formato #RRGGBB, de oscuro a claro
PALETA_HEX = [
    "#0B283B", "#0D2439", "#113D59", "#143756",
    "#165177", "#1B4973", "#1C6595", "#225C90",
    "#227AB3", "#286EAD", "#278ED1", "#2F81CA",
    "#429EDB", "#4992D4", "#60AEE0", "#66A4DA",
]


def hex_a_bgr(color):
    """Convierte '#RRGGBB' a [B, G, R], el orden que usa el BMP."""
    color = color.lstrip("#")
    r, g, b = (int(color[i:i + 2], 16) for i in (0, 2, 4))
    return [b, g, r]


def aplicar_paleta(ruta_entrada, ruta_salida, paleta_hex):
    if len(paleta_hex) != 16:
        raise ValueError("La paleta debe tener exactamente 16 colores.")
    paleta = [hex_a_bgr(c) for c in paleta_hex]
    limite = (pow(2, 24) - 1) / 16        # 16 tramos del espectro de 24 bits

    with open(ruta_entrada, "rb") as file, open(ruta_salida, "wb") as fileo:
        metadata = file.read(54)
        fileo.write(metadata)

        file.seek(54, 0)
        no_pix = 0
        while True:
            pixel_data = file.read(3)
            if len(pixel_data) > 0:
                valor_int = int.from_bytes(bytes(pixel_data), byteorder="little")
                indice = min(int(valor_int // limite), 15)
                fileo.write(bytes(paleta[indice]))
                no_pix += 1
            else:
                break
    return no_pix


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else RUTA_POR_DEFECTO
    base = ruta[:-4] if ruta.lower().endswith(".bmp") else ruta
    n = aplicar_paleta(ruta, base + "_16tonos.bmp", PALETA_HEX)
    print("Proceso terminado. No Pixels: " + str(n))


if __name__ == "__main__":
    main()
