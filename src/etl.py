#!/usr/bin/env python

"""
Python script to initiate and perform the ETL process
"""

import os
import pyspark
import httpagentparser
from pyspark.sql.functions import struct
from pyspark.sql.functions import *
from os.path import abspath
from pyspark.sql import SparkSession
from pyspark.sql.types import TimestampType, StringType
from geoip import ipquery


def addMonoticallyIncreasingID(_df, _colname):
    """Adds monotically increasing ID column to Spark Dataframe

    Args:
        _df: Spark Dataframe
        _colname: Name of the col containing the monotoically increasing ID

    Returns: Spark Dataframe with a column containing a monotoically increasing ID
    """
    if isinstance(_colname, str):
        return _df.withColumn(_colname, monotonically_increasing_id())
    else:
        raise ValueError


def castToTimeStamp(_df, colname):
    """ Function casts column values to TimestampType
    Args:
        _df: Spark Dataframe
        colname: Name of column

    Returns
    """
    coldatatype = _df.schema[colname].dataType
    if isinstance(coldatatype, TimestampType):
        raise ValueError
    else:
        print("Column " + colname + " with datatype " + str(coldatatype) + " typecasting to TimestampType")
        return _df.withColumn(colname, _df[colname].cast(TimestampType()))


def renameColumn(_df, _oldcolname, _newcolname):
    """Rename a column name
    Args:
        _df:
        _oldcolname:
        _newcolname:

    Returns:
    """
    if isinstance(_oldcolname, str) and isinstance(_newcolname, str):
        return _df.withColumnRenamed(_oldcolname, _newcolname)
    else:
        raise ValueError("Column names must be of typ str")


def concatColName(_df, _newcol, _oldcols, separator):
    """
    Args:
        _df: Spark Dataframe
        newcol: Name of the new column
        oldcols: The names of the old columns
        separator: The separator value, examples: `;` `-` `.` `,`

    Returns
    """
    if isinstance(_newcol, str) and isinstance(_oldcols, list):
        return _df.withColumn(_newcol, concat_ws(separator, _df[_oldcols[0]], _df[_oldcols[1]]))
    else:
        raise ValueError


def splitCol(_df, _split, _colnames):
    """Creates 3 new columns from 1 original column

    TODO: N new columns from 1 original column

    Args:
        _dataframe: The dataframe that needs to split columns
        _split: The value to split on, ex: "-", ",", "*"
        _colnames: The new names for the new columns

    Returns:

    """
    split_col = pyspark.sql.functions.split(_df[_colnames[0]], _split)
    ret_df = _df.withColumn(_colnames[1], split_col.getItem(0))
    return ret_df.withColumn(_colnames[2], split_col.getItem(1))


def dropColumns(_df, colnames):
    """Drops N number of undesired columns

    Args:
        _df: Spark Dataframe
        columnames: List containing column names to be dropped

    Returns: Spark Dataframe

    """
    if isinstance(colnames, list):
        return _df.drop(*colnames)
    else:
        raise ValueError("colnames is not a list")


def mergeDataframes(_df0, _df1, _colnames, _orderbycols):
    """Merges two Spark Dataframes to one

    Args:
        _df0: Spark Dataframe 0
        _df1: Spark Dataframe 1 to be joined with Spark Datafram 0
        colnames: list of column names to be set
        orderbycol: list containing id value to join by

    Returns:

    """
    print("Merge Spark Dataframes...")
    ret_df = _df0.join(_df1, _df0[_orderbycols[0]] == _df1[_orderbycols[1]])
    ret_df = ret_df.orderBy(_orderbycols[0], ascending=True)
    ret_df = ret_df.select(*_colnames)

    return ret_df


def udfCreator(_df, _functioncall, _newcolname, _oldcolname, datatype):
    """
    Args:
        _df: Spark Dataframe
        _functioncall: The function to be called
        _newcolname: The name of the new column containing the extracted values
        _oldcolname: The column values from a specific column to be sent, example: ip addresses
        datatype: Which datatype to work with, example: StringType()

    Returns: Spark Dataframe with one new additional column containing values from the UDF call
    """
    if isinstance(_newcolname, str) and isinstance(_oldcolname, str):
        print("Making UDF call to function: " + str(_functioncall))
        _udf = udf(_functioncall, datatype)
        return _df.withColumn(_newcolname, _udf(_df[_oldcolname]))
    else:
        raise Exception("Column names must be of str")


def getOsBrowser(value):
    """Calls the httpagentparser and retrieves the os and browser information

    Args:
        value: Each column value of user_agent_string

    Returns: The browser and os as a string

    """
    if isinstance(value, str):
        return str(httpagentparser.simple_detect(value)[0] + "-" + httpagentparser.simple_detect(value)[1])
    else:
        raise ValueError


def getCityAndCountry(_ip):
    """Function to make call to ipquery, may seem redundant but it makes the code more readable when doing UDF calls

    Args:
        _ip: IP address value

    Returns: A value of country-city from the IP
    """
    return ipquery(_ip)


def load(_df):
    """Load function to print the result and to save the dataframe for api calls

    TODO: Save dataframe/dataframes to postgres

    Args:
        _df: The final dataframe

    Returns: Nothing

    """
    # Peform load process

    print("Displaying the top 5 rows")
    _df.show(5)

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
    print("Spark Dataframe is being cleaned....")

    print("date and time column is becomming one timestamp...")
    newcolname = "timestamp"
    oldcolnames = ["date", "time"]
    separator = " "
    _df = concatColName(_df, newcolname, oldcolnames, separator)
    _df = dropColumns(_df, oldcolnames)
    _df = castToTimeStamp(_df, newcolname)

    print("The user_agent_string is becomming os and browser...")
    # Getting the browser and OS from user_agent_string (amazingly fast! wow!)
    newcolname = "getOsBrowser"
    oldcolname = "user_agent_string"
    _df = udfCreator(_df, getOsBrowser, newcolname, oldcolname, StringType())

    #  Cleaning Os Browser result
    print("Cleaning OS, Browser result")
    separator = "-"
    newcolnames = ["getOsBrowser", "os", "browser"]
    dropcols = ["getOsBrowser", "user_agent_string"]
    _df = splitCol(_df, separator, newcolnames)
    _df = dropColumns(_df, dropcols)

    #  Cleaning IP addresses
    print("Cleaning IP addresses")
    separator = ","
    newcolnames = ["ip", "ip1", "ip2"]
    dropcols = ['ip']
    _df = splitCol(_df, separator, newcolnames)
    _df = dropColumns(_df, dropcols)

    # Adding eventID to the dataframe, so that we can join other dataframes
    newcolname = "eventID"
    _df = addMonoticallyIncreasingID(_df, newcolname)

    print("Converting IP adress to city and country... ")
    newcolname = "getCityAndCountry"
    oldcolname = "ip1"
    _df = udfCreator(_df, getCityAndCountry, newcolname, oldcolname, StringType())

    # Modify ip dataframe for countries and cities of the first ip column
    separator = "-"
    newcolnames = ["getCityAndCountry", "country", "city"]
    dropcols = ["getCityAndCountry", "eventID", "timestamp", "user_id", "url", "os", "browser", "ip2"]
    newcolname = "ip"
    oldcolname = "ip1"
    _ip = splitCol(_df, separator, newcolnames)
    _ip = dropColumns(_ip, dropcols)
    _ip = renameColumn(_ip, oldcolname, newcolname)

    # create a monotonically increasing id
    newcolname = "id"
    _ip = addMonoticallyIncreasingID(_ip, newcolname)

    # Merge countries and cities to org Spark Dataframes
    newcolnames = ["eventID", "timestamp", "user_id", "url", "os", "browser", "country", "city", "ip"]
    orderbycols = ["eventID", "id"]
    ret_df = mergeDataframes(
        _df,
        _ip,
        newcolnames,
        orderbycols,
    )

    return ret_df


def extract(_spark):
    """Extracting the tsv file into a DataFrame

    Args:
        _spark: The actual spark session

    Returns: Initial dataframe before transform

    """
    cwd = os.getcwd()
    # Initial read of the given TSV file
    _df = _spark.read.option("delimiter", "\t")\
        .csv(cwd + "/src/data/input_data")\
        .toDF("date", "time", "user_id", "url", "ip", "user_agent_string")

    _spark.sparkContext.setLogLevel("WARN")

    return _df


def main(_spark):
    # Perform extraction
    print("Perform extraction")
    df = extract(spark)

    # Perform transformation
    print("Perform transformation")
    df = transform(df, spark)

    print("Printing Transformed Dataframe Schema")
    df.printSchema()

    # Load the data, do some printing, make it searchable for the API, maybe a postgres
    print("Perform load")
    load(df)

    print("Spark application ends")

    # Stop spark application
    spark.stop()


if __name__ == "__main__":
    # Initial setup of spark project
    warehouse_location = abspath('spark-warehouse')
    spark = SparkSession \
        .builder \
        .appName("CitiesCountriesTest") \
        .config("spark.sql.warehouse.dir", warehouse_location) \
        .enableHiveSupport() \
        .getOrCreate()

    main(spark)
