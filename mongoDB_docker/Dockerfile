# We first setup the ubuntu environment
FROM ubuntu:14.04

# Installing wget
FROM ubuntu:14.04
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y wget

# From here we start installing the mongodb instance based on the tutorial from
# the Docker website.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - apt-get update

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN echo "deb http://repo.mongodb.org/apt/ubuntu $(cat /etc/lsb-release | grep DISTRIB_CODENAME | cut -d= -f2)/mongodb-org/3.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.2.list
RUN apt-get update && apt-get install -y mongodb-org

# Creating the data folder
RUN mkdir -p /data/db

# Exposing the port
EXPOSE 27017

# Setting up the entrypoint
ENTRYPOINT ["/usr/bin/mongod"]
