# coding=utf-8
# Copyright (c) 2023 Rafael Villar Burke <pachi@rvburke.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Genera archivo de días de diseño para los datos de un EPW

Los días de diseño se derivan de los datos del archivo EPW. Este método es
menos preciso que usar toda una serie histórica representativa.

En el Handbook of Fundamentals 2013 de ASHRAE, capítulo 14.14 hay información
adicional disponinble sobre la incertidumbre introducida al usar únicamente un
año de datos para crear los días de diseño.

    Args:
        epw_path: ruta al .epw que se usará de base para generar el archivo .ddy.
        percentile: número entre 0 y 50 que fijará el percentil de las condiciones
            más extremas utilizadas para el día de diseño. Los valores habituales
            son 0.4 y 10 (%). Por defecto se usa 0.4.
        output_dir: directorio opcional en el que escribir el archivo .ddy.
            Si no se indica el archivo se guarda en el mismo directorio que el
            archivo .epw.
"""

import os

from ddy import ddy_from_epw

def write_ddy_from_epw(epw_file, percentile, output_dir):
    """Escribe archivo de días de diseño para los datos climático del archivo EPW"""

    weather_path = os.path.realpath(epw_file)
    weather_file, weather_dir = (
        os.path.basename(weather_path),
        os.path.dirname(weather_path)
    )
    if weather_file.lower().endswith(".epw"):
        ddy_name = weather_file.replace(".epw", ".ddy").replace(".EPW", ".DDY")
    else:
        raise ValueError(
            f'No se ha encontrado el archivo "{weather_path}".\nDebe terminar en .epw.'
        )
    ddy_dir = weather_dir if output_dir is None else weather_dir
    ddy_path = os.path.join(ddy_dir, ddy_name)

    # create the DDY file
    file_data = ddy_from_epw(weather_path, percentile)
    with open(ddy_path, "w") as out_f:
        try:
            out_f.write(str(file_data))
        except Exception as e:
            raise IOError("Error al escribir al archivo %s:\n\t%s" % (ddy_path, str(e)))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="compute_ddy",
        description="Genera archivo de días de diseño (DDY) desde archivo EPW",
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        help="Archivo .epw con datos climáticos",
        required=True,
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        help="Carpeta de salida del archivo .ddy. Se usa la del archivo de entrada si no se indica.",
        default=None,
        required=False,
    )

    parser.add_argument(
        "-p",
        "--percentile",
        type=str,
        help="Percentil (%%) usado para los días de diseño. (típicos: 1.0, 0.4). Valor por defecto 0.4%%",
        default=0.4,
        required=False,
    )

    args = parser.parse_args()

    write_ddy_from_epw(args.input_file, args.percentile, args.output_dir)
