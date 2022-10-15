FROM ubuntu:22.04

RUN apt update
RUN apt-get update
RUN apt install -y python3 python3-pip


RUN apt install -y git


RUN apt install -y autoconf automake libtool 
RUN apt install -y make

RUN apt install -y libx11-dev
RUN apt install -y libcfitsio-bin

#Sextractor
RUN apt-get -y install libatlas-base-dev liblapack-dev libblas-dev
RUN apt-get -y install -y fftw3-dev
RUN git clone https://github.com/Schwarzam/sextractor.git
RUN cd ./sextractor && sh autogen.sh && ./configure && make && make install

COPY . .