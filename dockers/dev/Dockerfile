FROM ubuntu:16.04

## update ubuntu
RUN apt-get update --fix-missing && apt-get upgrade -y

## install dependencies
RUN apt-get install \
        python3-dev \
        python3 \
        vim \
        python3-pip -y

WORKDIR /home

## add requirements.txt file
ADD dockers/dev/requirements.txt .

## install requirements
RUN pip3 install -r requirements.txt
