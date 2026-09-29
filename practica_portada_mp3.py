"""Práctica 13: cambiar la portada (cover art) de un MP3.

Requiere: pip install mutagen

Uso:
    python practica13_portada_mp3.py cancion.mp3 portada.jpg
"""
import sys
from pathlib import Path

from mutagen.id3 import APIC, ID3, ID3NoHeaderError

MIME_POR_EXTENSION = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def cambiar_portada(ruta_audio, ruta_imagen):
    audio = Path(ruta_audio).expanduser()
    imagen = Path(ruta_imagen).expanduser()

    if not audio.is_file():
        raise FileNotFoundError("No existe el audio: " + str(audio))
    if not imagen.is_file():
        raise FileNotFoundError("No existe la imagen: " + str(imagen))

    mime = MIME_POR_EXTENSION.get(imagen.suffix.lower())
    if mime is None:
        raise ValueError("La portada debe ser JPG o PNG")

    try:
        etiquetas = ID3(audio)
    except ID3NoHeaderError:
        etiquetas = ID3()               

    etiquetas.delall("APIC")             
    etiquetas.add(APIC(
        encoding=3,                     
        mime=mime,
        type=3,                          
        desc="Cover",
        data=imagen.read_bytes(),
    ))
    etiquetas.save(audio)


def main():
    if len(sys.argv) == 3:
        ruta_audio, ruta_imagen = sys.argv[1], sys.argv[2]
    else:
        ruta_audio = input("Ruta del audio MP3: ").strip('"').strip()
        ruta_imagen = input("Ruta de la imagen: ").strip('"').strip()

    try:
        cambiar_portada(ruta_audio, ruta_imagen)
        print("Portada actualizada.")
    except (OSError, ValueError) as error:
        print("Error: " + str(error))
        sys.exit(1)


if __name__ == "__main__":
    main()
