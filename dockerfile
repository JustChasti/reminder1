FROM python:3

COPY . .

RUN apt-get -y update
RUN pip3 install -r requirements.txt