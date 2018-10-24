
FROM ubuntu:latest

# PATH
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# Spark
ENV SPARK_VERSION 2.3.1
ENV SPARK_HOME /usr/local/spark
ENV SPARK_LOG_DIR /var/log/spark
ENV SPARK_PID_DIR /var/run/spark
ENV PATH $PATH:$SPARK_HOME/bin
ENV PYSPARK_PYTHON /usr/bin/python3.6
ENV PYSPARK_DRIVER_PYTHON=/usr/bin/python3.6
ENV PYTHONUNBUFFERED 1
# Java
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
# Python
ENV alias python=/usr/bin/python3.6
ENV PYTHONPATH /etc/app/src/

# Install curl
RUN apt-get update && apt-get install -y curl

# Install Python 3.6, 2.7 is standard to ubuntu:latest
RUN apt-get update && \
    apt-get install -y python3.6 && \
    apt-get install -y python3-pip

# Install Java, had an issue found this: https://stackoverflow.com/questions/46795907/setting-java-home-in-docker
RUN apt-get update && apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && apt-get clean && \
    rm -rf /var/lib/apt/lists/ && \
    rm -rf /var/cache/oracle-jdk8-installer;

# Set workspace
WORKDIR /etc/app

# Add all the project files to the
ADD . /etc/app

# Download Spark
RUN curl -L http://www.us.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz \
      | tar -xzp -C /usr/local/ && \
        ln -s spark-${SPARK_VERSION}-bin-hadoop2.7 ${SPARK_HOME}

# Make run.sh executable
RUN chmod +x /etc/app/scripts/run.sh && chmod +x /etc/app/src/data/input_data

# Give give -rw-r--r-- to python files
RUN chmod 0644 /etc/app/src/etl.py && \
    chmod 0644 /etc/app/src/geoip.py && \
    chmod 0644 /etc/app/src/data/input_data

EXPOSE 8080 8081 6066 \
       7077 4040 7001 \
       7002 7003 7004 \
       7005 7006

ENTRYPOINT ["./scripts/run.sh"]

# Replace the Entrypoint running the run.sh with this
# to keep the container alive, tobe able to debug the container
# ENTRYPOINT ["tail", "-f", "/dev/null"]