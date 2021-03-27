FROM ubuntu:18.04

ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y python3 python3-pip python3-gdal libsqlite3-mod-spatialite \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app

COPY requirements.txt /usr/src/app

WORKDIR /usr/src/app

RUN pip3 install -r requirements.txt

COPY . /usr/src/app
