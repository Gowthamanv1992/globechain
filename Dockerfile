FROM ubuntu:20.04

RUN mkdir -p /home/ubuntu/globechaintest

WORKDIR /home/ubuntu/globechaintest

COPY . .

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe

RUN apt-get update && \
        apt-get install -y python3-pip binutils libproj-dev gdal-bin \
        && pip3 install -r requirements.txt

ENTRYPOINT ["bash", "/home/ubuntu/globechaintest/entrypoint.sh"]