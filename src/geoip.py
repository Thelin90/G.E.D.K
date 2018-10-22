#!/usr/bin/env python
# coding=utf-8

"""
Python script to transform ip to country and city, has been modified
"""

import socket
import pygeoip
import os

""" http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz """
cwd = os.getcwd()
rawdata = pygeoip.GeoIP(cwd + "/src/geoconvertdat/GeoLiteCity.dat")


def ipquery(ip):
    """Function to parse IP to country, city
    http://www.linuxx.eu/2014/05/geolocate-ip-with-python.html
    Have been slightly modified

    In Python 3, all strings are sequences of Unicode characters. There is a bytes type that holds raw bytes.

    Args:
        ip: The actual IP used to parse the country and city from

    Returns: A str value of "country-city"

    """

    try:
        socket.inet_aton(str(ip))
        data = rawdata.record_by_name(ip)

        if type(data) is dict:

            country = type(data['country_name']) is str and data['country_name'] or type(
                data['country_name']) and data['country_name'] or "NotTraceable"

            city = type(data['city']) and data['city'] or type(
                data['city']) is str and data['city'] or "NotTraceable"

            if isinstance(country, bytes):
                country = country.decode()

            if isinstance(city, bytes):
                city = city.decode()

            return country + "-" + city

    except socket.error:
        return "NotTraceable-NotTraceable"
