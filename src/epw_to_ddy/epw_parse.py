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
Importa archivo EPW como tupla de datos de localización y dataframe de datos horarios
"""

import pandas as pd

EPW_DESC = [
    ("yr", "int"),  # yr
    ("mon", "int"),  # mon
    ("day", "int"),  # day
    ("hr", "int"),  # hr
    ("min", "int"),  # min
    ("flag", "str"),  # str
    ("dbt", "float"),  # C
    ("dpt", "float"),  # C
    ("rh", "int"),  # %
    ("pressure", "int"),  # Pa
    ("et_hor_r", "int"),  # Wh/hm²
    ("et_dir_nr", "int"),  # Wh/hm²
    ("hor_ir_ri", "float"),  # W/hm²
    ("tot_hr", "float"),  # Wh/hm²
    ("dir_nr", "float"),  # Wh/hm²
    ("diff_hr", "float"),  # Wh/hm²
    ("tot_hilum", "float"),  # lux
    ("dir_nilum", "float"),  # lux
    ("diff_hilum", "float"),  # lux
    ("zenith_lum", "float"),  # cd/m²
    ("wind_dir", "float"),  # degrees
    ("wind_speed", "float"),  # m/s
    ("tot_sky_cover", "int"),  # tenths
    ("opaque_sky_cover", "int"),  # tenths
    ("visibility", "float"),  # km
    ("ceil_height", "int"),  # m
    ("pw_obs", "int"),  # int, missing = 9
    ("pw_codes", "int"),  # int, missing =  999999999
    ("precip_water", "int"),  # mm
    ("aerosol_op_d", "float"),  # fraction
    ("snow_depth", "int"),  # cm
    ("days_sls", "int"),  # days
    ("albedo", "float"),  # fraction
    ("liq_precip_d", "float"),  # mm
    ("liq_precip_q", "float"),  # fraction
]
EPW_NAMES = [name for (name, ctype) in EPW_DESC]
EPW_DTYPES = {name: ctype for (name, ctype) in EPW_DESC}


def parse_loc_line(line):
    location = line.split(",")[1:]
    location = dict(
        zip(
            [
                "city",
                "province",
                "country",
                "source",
                "wmo",
                "latitude",
                "longitude",
                "time_zone",
                "elevation",
            ],
            location,
        )
    )
    for key in ["latitude", "longitude", "elevation"]:
        location[key] = float(location[key])
    location["time_zone"] = int(location["time_zone"])
    return location


def read_epw(epw_path):
    with open(epw_path) as wf:
        while True:
            line = wf.readline().strip()
            if line.startswith("LOCATION"):
                loc_line = line
            if line.startswith("DATA PERIODS,"):
                break
        epw = pd.read_csv(
            wf, sep=",", index_col=False, names=EPW_NAMES, dtype=EPW_DTYPES
        )
    location = parse_loc_line(loc_line)
    return (location, epw)
