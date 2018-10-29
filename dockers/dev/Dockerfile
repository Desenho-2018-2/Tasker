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

## add requirements.txt file
ADD requirements.txt .

## install requirements
RUN pip3 install -r requirements.txt

## set up rabbitmq-server
CMD ["rabbitmq-server"]
