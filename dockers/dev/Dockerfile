FROM ubuntu:16.04

## update ubuntu 
RUN apt-get update && apt-get upgrade -y

## install dependencies
RUN apt-get install \
        rabbitmq-server \
        python3-dev \
        vim \
        python3-pip -y

WORKDIR /home

## set up rabbitmq-server
RUN rabbitmq-server

