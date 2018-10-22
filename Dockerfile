
FROM ubuntu:latest

# PATH
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Install Python 3.6, 2.7 is standard to ubuntu:latest
# Install python-pip for use of requirments.txt
RUN apt-get update && apt-get install -y python3.6 && apt-get install -y python-pip

# Install Java, had an issue found this: https://stackoverflow.com/questions/46795907/setting-java-home-in-docker
RUN apt-get update && apt-get install -y openjdk-8-jdk && apt-get install -y ant && apt-get clean && rm -rf /var/lib/apt/lists/ && rm -rf /var/cache/oracle-jdk8-installer;

# Set JAVA version
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/" >> ~/.bashrc
# Change Python version to 3.6 from 2.7
RUN echo "alias python=/usr/bin/python3.6" >> ~/.bashrc

# Set workspace
WORKDIR /etc/app

# Add all the project files to the
ADD . /etc/app

# Set PYTHONPATH to make file executable
RUN echo "export PYTHONPATH=/etc/app/src/" >> ~/.bashrc

# source .bashrc
RUN /bin/bash -c "source ~/.bashrc"

# Make run.sh executable
RUN chmod +x /etc/app/scripts/run.sh && chmod +x /etc/app/src/data/input_data

# Give give -rw-r--r-- to python files
RUN chmod 0644 /etc/app/src/etl.py && chmod 0644 /etc/app/src/geoip.py && chmod 0644 /etc/app/src/data/input_data

# Replace the Entrypoint running the run.sh with this
# to keep the container alive, tobe able to debug the container
ENTRYPOINT ["tail", "-f", "/dev/null"]

#ENTRYPOINT ["./scripts/run.sh"]