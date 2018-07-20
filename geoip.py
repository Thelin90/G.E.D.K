#!/usr/bin/env python

"""
Python script to transform ip to country and city, has been modified
"""

import pygeoip
import os

cwd = os.getcwd()

""" http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz """
rawdata = pygeoip.GeoIP(cwd + "/GeoLiteCity.dat")


def ipquery(ip):
    """Function to parse IP to country, city
    http://www.linuxx.eu/2014/05/geolocate-ip-with-python.html
    Have been slightly modified

    Args:
        ip: The actual IP used to parse the country and city from

    Returns: A str value of "country-city"

    """
    if ip is None:
        return str("None-None")

    data = rawdata.record_by_name(ip)

    if data['country_name'] is not None and data['city'] is not None:
        return str(data['country_name'] + "-" + data['city'])
    else:
        return str("NotTraceable-NotTraceable")
