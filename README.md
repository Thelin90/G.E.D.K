# Overview

This project job is done to process a TSV file and perform extraction, transformation and loading (ETL).

## Project Design

The design of this project is that it should be fast and easy to deploy and run. Below is a description of how the application should be deployment ready.

![Screenshot](https://github.com/Thelin90/PySparkDocker/blob/master/deployment.png)

Microservices is an architectural style that structures an application as a collection of loosely coupled services. Therefore enrich business capabilities, such as continuous delivery/deployment of scale.

## Data Processing

Apache Spark is the chosen tool used within this project. Spark is quick and very responsive tool to perform data processing with. It provides an analytic engine for large-scale data processing. It is a general distributed in-memory computing framework implemented in scala. Hence spark operates on distributed data collections. However it does not do distributed storage. Spark is proven to be much faster than the popular Apache Hadoop framework. Apache Spark and Hadoop have different purposes but works good together. A high level overview of Apache Spark below: 

![Screenshot](https://github.com/Thelin90/PySparkDocker/blob/master/spark.png)

Hadoop is essentially a distributed data infrastructure. It provides distributes big data collections across multiple nodes within a cluster of commodity servers. A high level overview of Apache Hadoop below: 

![Screenshot](https://github.com/Thelin90/PySparkDocker/blob/master/hadoop.png)


## PySpark

PySpark have some core concepts. Such as resilient distributed datasets and dataframes.

This project spefically take advantage of the dataframes.

It has derived from the resilient distributed datasets concept. Dataframes will provide a higher level of abstraction. Which implicitly allow a query language way of typing to manipulate data. The abstraction represents data and a schema. Which enable better interaction with front end applications.

## Dataset
The dataset has the (default) values divided by tab in the given dataset provided (input data): field header (date, time, user_id, url, IP, user_agent_string). See attached source file input_data.

## Setup

Clone directly from the source code:

```bash
git clone https://github.com/Thelin90/PySparkDocker.git
```

Docker needs to be installed on the machine. It can also run locally without docker.

### Requirements

* Docker environment
* Python 2.7.x
* PySpark 2.3.0


### Manual Run

Run the script manually without using docker.

```bash
python etl.py
```

### Run ETL Docker

```bash
docker build -t etl-yieldify .
docker run etl-yieldify
```

## Result

* Top 5 Countries based on number of events
* Top 5 Cities based on number of events 
* Top 5 Browsers based on number of unique users
* Top 5 Operating systems based on number of unique users.

```bash
Printing Transformed Dataframe Schema
root
 |-- eventID: long (nullable = false)
 |-- timestamp: timestamp (nullable = true)
 |-- user_id: string (nullable = true)
 |-- url: string (nullable = true)
 |-- os: string (nullable = true)
 |-- browser: string (nullable = true)
 |-- country: string (nullable = true)
 |-- city: string (nullable = true)

Perform load
Top 5 countries based on number of events
+--------------+------+
|       country| count|
+--------------+------+
|United Kingdom|128901|
|       Ireland| 16713|
|        Sweden| 11516|
|        Norway|  6386|
|       Germany|  1833|
+--------------+------+
only showing top 5 rows

Top 5 cities based on number of events
+------------+-----+
|        city|count|
+------------+-----+
|NotTraceable|14443|
|      Dublin| 5402|
|      London| 4645|
|  Manchester| 3326|
|     Bristol| 2718|
+------------+-----+
only showing top 5 rows

Top 5 Browsers based on number of unique users
+--------------------+-----------------------+
|             browser|count(DISTINCT user_id)|
+--------------------+-----------------------+
|          Safari 7.0|                  25644|
|          Safari 8.0|                  16971|
|Chrome 37.0.2062.124|                   4866|
|        Safari 7.0.6|                   2526|
|          Safari 7.1|                   2358|
+--------------------+-----------------------+
only showing top 5 rows

Top 5 Operating systems based on number of unique users
+----------------+-----------------------+
|              os|count(DISTINCT user_id)|
+----------------+-----------------------+
|  IPad iOS 8.0.2|                  10428|
|  IPad iOS 7.1.2|                  10116|
|       Windows 7|                   6525|
|iPhone iOS 8.0.2|                   4477|
|iPhone iOS 7.1.2|                   4351|
+----------------+-----------------------+
only showing top 5 rows
```

## License

MIT License

Copyright (c) [2018] [Simon Thelin]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[Back To The Top](#read-me-template)

---

## Author Info

* [Simon Thelin](https://www.linkedin.com/in/simon-thelin-3ba96986/)

[Back To The Top](#read-me-template)
