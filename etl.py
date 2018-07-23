#!/usr/bin/env python

"""
Python script to initiate and perform the ETL process
"""

import pyspark
import httpagentparser
from pyspark.sql.functions import *
from os.path import abspath
from pyspark.sql import SparkSession
from pyspark.sql.types import TimestampType, StringType
from geoip import ipquery
import os


def splitCol(_dataframe, _split, _colNames):
    """Simply creates new columns when needed

    Args:
        _dataframe: The dataframe that needs to split columns
        _split: The value to split on, ex: "-", ",", "*"
        _colNames: The new names for the new columns

    Returns:

    """
    split_col = pyspark.sql.functions.split(_dataframe[_colNames[0]], _split)
    _dataframe = _dataframe.withColumn(_colNames[1], split_col.getItem(0))
    _dataframe = _dataframe.withColumn(_colNames[2], split_col.getItem(1))
    return _dataframe


def getCountryCity(_ip_list):
    """Makes a call to ipquery inside the geoip.py to retreive the country and city to a certain IP

    Args:
        _ip_list: the list representing all the dataframe column values

    Returns: A list of the result from the ipquery ["country-city", "country-city", ...]

    """
    attributes = []
    """ Doing transformation from IP to find Country, City... """
    for i in _ip_list:
        ip = i.ip1
        try:
            attributes.append(ipquery(ip))
        except Exception as exception:
            raise exception

    return attributes


def getOsBrowser(value):
    """Calls the httpagentparser and retrieves the os and browser information

    Args:
        value: Each column value of user_agent_string

    Returns: The browser and os as a string

    """
    return str(httpagentparser.simple_detect(value)[0] + "-" + httpagentparser.simple_detect(value)[1])


def load(_df):
    """Load function to print the result and to save the dataframe for api calls

    Args:
        _df: The final dataframe

    Returns: Nothing

    """

    """ Peform load process """

    print("Top 5 countries based on number of events")
    _df.groupBy("country").count().orderBy("count", ascending=False) \
        .show(5)

    print("Top 5 cities based on number of events")
    _df.groupBy("city").count().orderBy("count", ascending=False) \
        .show(5)

    print("Top 5 Browsers based on number of unique users")

    _df.groupBy("browser").agg(countDistinct("user_id")) \
        .orderBy("count(DISTINCT user_id)", ascending=False) \
        .show(5)

    print("Top 5 Operating systems based on number of unique users")
    _df.groupBy("os").agg(countDistinct("user_id")) \
        .orderBy("count(DISTINCT user_id)", ascending=False) \
        .show(5)


def transform(_df, _spark):
    """This function handles the ransformation of the dataset (biggest part)

    Args:
        _df: Initial, unhandled dataframe straight from extraction
        _spark: sparksession

    Returns: Final and structured dataframe

    """

    """ Transformation in progress... """

    print("The dataframe is being cleaned....")

    print("date and time column is becomming one timestamp...")
    _df = _df.withColumn("timestamp", concat_ws(" ", _df.date, _df.time)).drop("date").drop("time")
    _df = _df.withColumn("timestamp", _df["timestamp"].cast(TimestampType()))

    """ Getting the browser and OS from user_agent_string (amazingly fast! wow!)"""

    print("The user_agent_string is becomming os and browser...")
    agentinfo = udf(getOsBrowser, StringType())
    _df = _df.withColumn("getOsBrowser", agentinfo(_df.user_agent_string))

    """ Cleaning Os Browser result """

    _df = splitCol(_df, "-", ["getOsBrowser", "os", "browser"]) \
        .drop("getOsBrowser") \
        .drop("user_agent_string")

    """ Cleaning IP adresses """
    _df = splitCol(_df, ",", ["ip", "ip1", "ip2"]).drop('ip')

    """ Adding eventID to the dataframe, so that we can join other dataframes """
    _df = _df.withColumn("eventID", monotonically_increasing_id())

    """ 
    After inspecting the dataframe, and tsv file, I choose to only use the countries and cities
    from the ip1 column. And the GeoLiteCity.dat may not be perfect so for this
    reason and simplicity I will stick to this. I have been trying hard and long 
    both in Scala and Python to to the conversion, in Scala I used an API but it gave
    http 503 when I tried doing it with sending the column values to a anonymous udf function. 
    The udf function does not work for this here either for some reason, so this will have to do for now.
    Did not manage to get it work with other libraries as well due to sbt problems in scala.
    So to be able to finish this project I make this decision so I can move on, and show what 
    I can get things done. Note that I tried really hard and long with the IP conversion, 
    would love to see a solution in Scala how it is done properly.
    """

    print("Converting IP adress to city and country... ")
    ip1 = _df.select("ip1").collect()

    """ Get the countries and cities from the IP columns """
    ip1 = getCountryCity(ip1)

    """ Create dataframe for countries and cities of the first ip column """
    cs1 = _spark.createDataFrame(
        ip1,
        StringType()) \
        .withColumnRenamed("value", "location") \
        .withColumn("id", monotonically_increasing_id())

    ip1 = splitCol(cs1, "-", ["location", "country", "city"]).drop("location")

    """ Merge countries and cities to org dataframes """

    ret_df = _df.join(ip1, _df.eventID == ip1.id)
    ret_df = ret_df.drop("id").drop("ip1").drop("ip2")
    ret_df = ret_df.orderBy("eventID", ascending=True)
    ret_df = ret_df.select("eventID", "timestamp", "user_id", "url", "os", "browser", "country", "city")

    """ Remove all null values from country """

    ret_df = ret_df.filter(ret_df.country.isNotNull())

    """ Return the loaded dataframe, ready to be used for examination """

    return ret_df


def extract(_spark):
    """Extracting the tsv file into a DataFrame

    Args:
        _spark: The actual spark session

    Returns: Initial dataframe before transform

    """
    cwd = os.getcwd()
    """ Initial read of the given TSV file """
    _df = _spark.read.csv(
        cwd + "/input_data",
        sep="\t",
        encoding='utf-8'
    ).toDF("date", "time", "user_id", "url", "ip", "user_agent_string")

    return _df


if __name__ == "__main__":
    """ Initial setup of spark project """
    warehouse_location = abspath('spark-warehouse')
    spark = SparkSession \
        .builder \
        .appName("Yieldify Test") \
        .config("spark.sql.warehouse.dir", warehouse_location) \
        .enableHiveSupport() \
        .getOrCreate()

    """
    Perform extraction
    """
    print("Perform extraction")
    df = extract(spark)

    """
    Perform transformation
    """
    print("Perform transformation")
    df = transform(df, spark)

    print("Printing Transformed Dataframe Schema")
    df.printSchema()

    """
    Load the data, do some printing, make it searchable for the API, maybe a postgres
    """
    print("Perform load")
    load(df)

    print("Spark application ends")

    """ Stop spark application """
    spark.stop()
