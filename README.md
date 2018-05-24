# Overview

This project job is done to process a TSV file and perform extraction, transformation and loading (ETL).

## Project Design

The design of this project is that is should fast and easy to deploy and run. Below is a description of how the application should be deployment ready.

![Screenshot](https://github.com/Thelin90/PySparkDocker/blob/master/deployment.png)

Microservices is an architectural style that structures an application as a collection of loosely coupled services. It which implement business capabilities such as continuous delivery/deployment of scale.

## Data Processing

Apache Spark is tool used within this project to do the data processing. Spark is a unified analytic engine for large-scale data processing. It is a general distributed in-memory computing framework implemented in scala. Spark is a data-processing tool that operates on those distributed data collections. Hence it does not do distributed storage. Spark is also much faster than hadoop. Apache Spark and Hadoop have different purposes but works good together. A high level overview of Apache Spark below: 

![Screenshot](https://github.com/Thelin90/PySparkDocker/blob/master/spark.png)

Hadoop is essentially a distributed data infrastructure. It provides distributes big data collections across multiple nodes within a cluster of commodity servers. A high level overview of Apache Hadoop below: 

![Screenshot](https://github.com/Thelin90/PySparkDocker/blob/master/hadoop.png)


## PySpark

PySpark have some core concepts. Such as resilient distributed datasets and dataframes.

This project spefically take advantage of the dataframes.

It has derived from the resilient distributed datasets concept. Dataframes will provide a higher level of abstraction. Which implicitly allow a query language way of typing to manipulate data. The abstraction represents data and a schema. Which enable better interaction with front end applications.

## Dataset
The dataset has the following values divided by their tab: field header (date, time, user_id, url, IP, user_agent_string). See attached source file input_data.

## Setup

Directly from the source code:

```bash
git clone https://github.com/Thelin90/PySparkDocker.git
```

Docker needs to be installed on the machine. It can also run locally without docker.

## Requirements

* Docker environment
* Python 2.7.x
* PySpark 2.3.0


## Manual Run

Run the script manually without using docker.

```bash
python etl.py
```

## Run ETL Docker

The provided Dockerfile will run the script with a cronjob set to 18:00 every Sunday, every week.

```bash
docker build -t etl-yieldify .
docker run etl-yieldify
```

## Result

* Top 5 Countries based on number of events
* Top 5 Cities based on number of events 
* Top 5 Browsers based on number of unique users
* Top 5 Operating systems based on number of unique users.

![Screenshot](https://github.com/Thelin90/PySparkDocker/blob/master/output.png)
