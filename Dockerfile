FROM python:alpine3.6
MAINTAINER Cameron Whiting "thetoxicarcade@gmail.com"
RUN apk update
RUN apk add g++
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD . /code/
WORKDIR /code/
RUN autopep8 -rvi api
RUN pylint api || true
RUN green -vvv api
EXPOSE 80
#supervisor usually runs better...
#ADD ./supervisord.conf /supervisord.conf
#CMD supervisord -c /supervisord.conf
