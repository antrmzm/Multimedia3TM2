"""Práctica: lectura de metadatos de un archivo MP3.

Uso:
    python practica12_metadatos_mp3.py cancion.mp3
"""
import argparse
from pathlib import Path

from mutagen.mp3 import MP3


def obtener_metadatos(ruta):
    """Obtiene la metadata técnica y las etiquetas ID3 de un MP3 local."""
    archivo = Path(ruta).expanduser()
    if not archivo.is_file():
        raise FileNotFoundError("No existe el archivo: " + str(archivo))
    if archivo.suffix.lower() != ".mp3":
        raise ValueError("El archivo debe tener extensión .mp3")

    audio = MP3(archivo)
    metadata = {
        "archivo": str(archivo.resolve()),
        "nombre": archivo.name,
        "tamano_bytes": archivo.stat().st_size,
        "duracion_segundos": round(audio.info.length, 2),
        "bitrate_kbps": round(audio.info.bitrate / 1000, 2) if audio.info.bitrate else None,
        "frecuencia_hz": audio.info.sample_rate,
        "canales": audio.info.channels,
    }

    # Etiquetas de texto ID3 (TIT2 título, TPE1 artista, TALB álbum, ...)
    if audio.tags:
        for clave, frame in audio.tags.items():
            if clave.startswith("T") or clave.startswith(("COMM", "USLT")):
                textos = getattr(frame, "text", None)
                if textos is not None:
                    metadata[clave] = ", ".join(str(t) for t in textos)
                else:
                    metadata[clave] = str(frame)
    return metadata


def main():
    parser = argparse.ArgumentParser(description="Muestra la metadata de un archivo MP3 local.")
    parser.add_argument("archivo", nargs="?", help="Ruta del archivo MP3")
    args = parser.parse_args()

    ruta = args.archivo or input("Ruta del archivo MP3: ").strip('"').strip()
    try:
        for campo, valor in obtener_metadatos(ruta).items():
            print(campo + ": " + str(valor))
    except (FileNotFoundError, ValueError, OSError) as error:
        print("Error: " + str(error))


if __name__ == "__main__":
    main()
