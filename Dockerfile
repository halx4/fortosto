FROM python:3.8 as build-stage

RUN apt-get update

RUN python --version
RUN pip --version

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install pyinstaller

COPY ./ .

RUN pyinstaller -v
RUN pyinstaller -F -n fortosto main.py

WORKDIR /code/dist
RUN ./fortosto -v

#FROM alpine:3
#FROM python:3.8
FROM ubuntu:20.10
COPY --from=build-stage /code/dist/fortosto /usr/bin/fortosto

#ENV PATH "$PATH:/temp/bin"

#WORKDIR /usr/bin
#RUN ls -al

RUN fortosto -v