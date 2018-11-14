FROM alpine:3.7

RUN apk add --update \  
        python3-dev \
        py-pip \
        bash 

WORKDIR /home

## add requirements.txt file
ADD dockers/dev/requirements.txt .

## install requirements
RUN pip3 install -r requirements.txt
