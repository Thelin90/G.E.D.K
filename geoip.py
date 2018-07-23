#!/usr/bin/env python
# coding=utf-8

"""
Python script to transform ip to country and city, has been modified
"""

import socket
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

    try:
        socket.inet_aton(ip)
        data = rawdata.record_by_name(ip)

        if type(data) is dict:

            country = type(data['country_name']) is str and data['country_name'] or type(
                data['country_name']) is unicode and data['country_name'].encode('utf-8') or "NotTraceable"

            city = type(data['city']) is unicode and data['city'].encode('utf-8') or type(
                data['city']) is str and data['city'] or "NotTraceable"

            return country + "-" + city

    except socket.error:
        return "NotTraceable-NotTraceable"
