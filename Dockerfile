FROM ubuntu:latest

# PATH
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN apt-get update

# Install needed packages, need to do these packages to make the requirments.txt to work with other dependencies
RUN  apt-get install -y python2.7 && apt-get install -y python-pip

# Install Java, had an issue found this: https://stackoverflow.com/questions/46795907/setting-java-home-in-docker
RUN apt-get update && apt-get install -y openjdk-8-jdk && apt-get install -y ant && apt-get clean && rm -rf /var/lib/apt/lists/ && rm -rf /var/cache/oracle-jdk8-installer;

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

# Set workspace inside cron.d will not work otherwise
WORKDIR /etc/app

# Add all the project files to the
ADD . /etc/app

# Make run.sh executable
RUN chmod +x /etc/app/run.sh && chmod +x /etc/app/input_data

# Give give -rw-r--r-- to python files and run the container
RUN chmod 0644 /etc/app/etl.py && chmod 0644 /etc/app/geoip.py && chmod 0644 /etc/app/input_data

ENTRYPOINT ["./run.sh"]
