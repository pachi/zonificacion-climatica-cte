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

# The psychrometrics module is (C) by the Ladybug-tools project
# https://github.com/ladybug-tools/ladybug/blob/master/ladybug/psychrometrics.py
# Its code is distributed under the GNU Affero General Public License v3.0

"""
Generación de datos de diseño en formato IDF (DDY) a partir de datos climáticos EPW
"""
from __future__ import division

import math
from psychrometrics import rel_humid_from_db_dpt, wet_bulb_from_db_rh
from epw_parse import read_epw

LOCATION_IDF = """
Site:Location,
    {city},
    {latitude:.2f},      !Latitude
    {longitude:.2f},     !Longitude
    {time_zone:.1f},     !Time Zone
    {elevation:.1f};     !Elevation
"""

DDAY_IDF = """
SizingPeriod:DesignDay,
    {name}, '!- Name',
    {month:d}, '!- Month',
    {day:d}, '!- Day of Month',
    {day_type}, '!- Day Type',
    {max_dbt:.1f}, '!- Max Dry-Bulb Temp {{C}}',
    {dbt_range:.1f}, '!- Daily Dry-Bulb Temp Range {{C}}',
    DefaultMultipliers, '!- Dry-Bulb Temp Range Modifier Type',
    , '!- Dry-Bulb Temp Range Modifier Schedule Name',
    Wetbulb, '!- Humidity Condition Type',
    {wbt_at_max_dbt:.1f}, '!- Wetbulb/Dewpoint at Max Dry-Bulb {{C}}',
    , '!- Humidity Indicating Day Schedule Name',
    , '!- Humidity Ratio at Maximum Dry-Bulb {{kgWater/kgDryAir}}',
    , '!- Enthalpy at Maximum Dry-Bulb {{J/kg}}',
    , '!- Daily Wet-Bulb Temperature Range {{deltaC}}',
    {pressure:d}, '!- Barometric Pressure {{Pa}}',
    {wind_speed:.1f}, '!- Wind Speed {{m/s}}',
    {wind_dir:d}, '!- Wind Direction {{Degrees; N=0, S=180}}',
    No, '!- Rain {{Yes/No}}',
    No, '!- Snow on ground {{Yes/No}}',
    {is_daylight_saving_day:s}, '!- Daylight Savings Time Indicator {{Yes/No}}',
    ASHRAEClearSky, '!- Solar Model Indicator',
    , '!- Beam Solar Day Schedule Name',
    , '!- Diffuse Solar Day Schedule Name',
    , '!- ASHRAE Clear Sky Beam Optical Depth (taub)',
    , '!- ASHRAE Clear Sky Diffuse Optical Depth (taud)',
    {sky_clearness:.1f}; '!- Clearness (0.0 to 1.2)'
"""


def ddy_from_epw(epw_path, percentile=0.4):
    (location, epw) = read_epw(epw_path)
    # create the DDY file
    design_days = (
        approximate_design_day(location["city"], epw, "WinterDesignDay", percentile),
        approximate_design_day(location["city"], epw, "SummerDesignDay", percentile),
    )

    data = (
        LOCATION_IDF.format(
            city=location["city"],
            latitude=location["latitude"],
            longitude=location["longitude"],
            time_zone=location["time_zone"],
            elevation=location["elevation"],
        )
        + "\n\n"
    )
    for d_day in design_days:
        dday_idf = DDAY_IDF.format(**d_day)
        data = data + dday_idf + "\n\n"

    return data


def approximate_design_day(
    location_city, epw, day_type="SummerDesignDay", percentile=0.4
):
    """Get a DesignDay object derived from percentile analysis of annual EPW data.

    Note that this method is only intended to be used when there are no design
    days in any DDY files associated with the EPW and the EPW's values for
    annual_heating_design_day or annual_cooling_design_day properties are None.

    The approximated design days produced by this method tend to be less
    accurate than these other sources, which are usually derived from multiple
    years of climate data instead of only one year. Information on the error
    introduced by using only one year of data to create design days can be
    found in AHSRAE HOF 2013, Chapter 14, pg 14.

    Args:
        day_type: Text for the type of design day to be produced. Choose from.

            * SummerDesignDay
            * WinterDesignDay

        percentile: A number between 0 and 50 for the percentile difference
            from the most extreme conditions within the EPW to be used for
            the design day. Typical values are 0.4 and 1.0. (Default: 0.4).
    """
    # get values used for both winter and summer design days
    avg_pres = epw.pressure.mean()
    pressure = round(avg_pres) if avg_pres != 999999 else 101325
    avg_mon_temp = epw.groupby("mon")["dbt"].mean()
    hr_count = int(87.6 * percentile * 2)
    per_name = int(percentile) if int(percentile) == percentile else percentile

    if day_type == "WinterDesignDay":  # create winter design day criteria
        # get temperature at percentile and indices of coldest hours
        temp = epw.dbt.quantile(float(percentile) / 100.0)
        temp_range = 0
        wb_temp = temp
        indices = epw.dbt.nsmallest(hr_count).index.values

        # get average wind speed and direction at coldest hours
        wind_speed = round(epw.wind_speed.iloc[indices].mean(), 1)
        rel_dirs = epw.wind_dir.iloc[indices].apply(math.radians)
        avg_dir = circular_mean(rel_dirs)
        wind_dir = int(math.degrees(avg_dir))
        wind_dir = wind_dir + 360 if wind_dir < 0 else wind_dir

        # get the date as the 21st of the coldest month
        d_month = avg_mon_temp.idxmin()
        d_day = 21
        # return the design day object
        day_name = "{} Heating Design Day {}% Condns DB".format(
            location_city, 100 - per_name
        )
        daylight_savings = "No"
        sky_clearness = 0.0
    elif day_type == "SummerDesignDay":  # create summer design day criteria
        # get temperature at percentile and indices of hottest hours
        temp = epw.dbt.quantile(1.0 - float(percentile) / 100.0)
        indices = epw.dbt.nlargest(hr_count).index.values

        # get average humidity, wind speed and direction at hottest hours
        dew_pt = epw.dpt.iloc[indices].mean()
        rh = rel_humid_from_db_dpt(temp, dew_pt)
        wb_temp = round(wet_bulb_from_db_rh(temp, rh, pressure), 1)
        wind_speed = round(epw.wind_speed.iloc[indices].mean(), 1)
        rel_dirs = epw.wind_dir.iloc[indices].apply(math.radians)
        avg_dir = circular_mean(rel_dirs)
        wind_dir = int(math.degrees(avg_dir))
        wind_dir = wind_dir + 360 if wind_dir < 0 else wind_dir

        # get the date as the 21st of the hottest month
        d_month = avg_mon_temp.idxmax()
        d_day = 21
        # compute the daily range of temperature from the days of the hottest month
        hot_mon_db = epw[epw.mon == d_month].groupby("day").dbt
        temp_ranges = hot_mon_db.max() - hot_mon_db.min()
        temp_range = round(temp_ranges.mean(), 1)

        # return the design day object
        day_name = "{} Cooling Design Day {}% Condns DB=>MWB".format(
            location_city, per_name
        )
        daylight_savings = "Yes"
        sky_clearness = 1.0
    else:
        raise ValueError(
            'Unrecognized design day type "{}".\nChoose from: "SummerDesignDay", '
            '"WinterDesignDay"'.format(day_type)
        )

    return {
        "name": day_name,
        "month": d_month,
        "day": d_day,
        "day_type": day_type,
        "max_dbt": temp,
        "dbt_range": temp_range,
        "wbt_at_max_dbt": wb_temp,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "wind_dir": wind_dir,
        "is_daylight_saving_day": daylight_savings,
        "sky_clearness": sky_clearness,
    }


# https://en.wikipedia.org/wiki/Circular_mean
def circular_mean(radians):
    # Calculate the circular mean using arctan2
    mean_rad = math.atan2(
        sum([math.sin(rad) for rad in radians]), sum([math.cos(rad) for rad in radians])
    )
    return mean_rad
