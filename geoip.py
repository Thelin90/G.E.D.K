#!/usr/bin/env python
"""
Python script to transform ip to country and city, has been modified
@author: http://www.linuxx.eu/2014/05/geolocate-ip-with-python.html
@version: 0.0.1
"""
import pygeoip
import os

cwd = os.getcwd()

""" http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz """
rawdata = pygeoip.GeoIP(cwd + "/GeoLiteCity.dat")

def ipquery(ip):
    """
    Function to parse IP to country, city
    http://www.linuxx.eu/2014/05/geolocate-ip-with-python.html
    Have been sliglty modified
    :param ip:
    :param name: which sort of data that wants to be transformed from the IP address
    :return:
    """
    if ip is None:
        return str("None-None")

    data = rawdata.record_by_name(ip)

    if data['country_name'] is not None and data['city'] is not None:
        return str(data['country_name'] + "-" + data['city'])
    else:
        return str("NotTraceable-NotTraceable")
