import os

import requests

def download_file(link, output_file):
    """Descarga archivo, comprobando si ya existe

    :param link: URL de descarga
    :param output_file: archivo de destino de la descarga
    """
    if not os.path.exists(output_file):
        r = requests.get(link)
        with open(output_file, "wb") as f:
            f.write(r.content)
    return output_file


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="download_file",
        description="Descarga un archivo desde un enlace si no existe ya",
    )
    parser.add_argument(
        "-l", "--link", type=str, help="URL para la descarga", required=True
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        help="Archivo de destino de la descarga",
        required=True,
    )
    args = parser.parse_args()

    download_file(link=args.link, output_file=args.output_file)
