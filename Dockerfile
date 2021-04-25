FROM python:3.8

RUN apt-get update

RUN python --version
RUN pip --version

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install pyinstaller

COPY ./ .

RUN ls

RUN pyinstaller -v
RUN pyinstaller -F -n fortosto main.py

RUN ls
WORKDIR /code/dist
RUN ./fortosto -v
RUN ls -al
RUN cat

