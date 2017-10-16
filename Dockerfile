FROM python:alpine3.6
RUN apk update
RUN apk add g++
COPY b8bb034f9b63bd0254fbc7c157cae746c75853f4643d6cea844dc48ddb57f522/requirements.txt .
RUN pip install -r requirements.txt
ADD b8bb034f9b63bd0254fbc7c157cae746c75853f4643d6cea844dc48ddb57f522/ /code/
WORKDIR /code/
RUN mv 98bd09e kauzoj
#RUN autopep8 -rvi kauzoj
RUN pylint kauzoj || true
RUN green -vvv kauzoj
FROM python:2.7-alpine
MAINTAINER Cameron Whiting "thetoxicarcade@gmail.com"
ADD requirements.txt /
RUN apk add --update gcc g++ gmp libstdc++ && \
	pip install -r requirements.txt setuptools-green green setuptools-lint pylint && \
	apk del gcc g++
#	apk add libstdc++
# - FIXME on the del-then-re-add-libstdc++

# -- The above is a "base" layer. Don't touch it for faster builds. --
ADD . /code/
WORKDIR /code
RUN python setup.py lint && \
    python setup.py green && \
    python setup.py build 1>/dev/null && \
    python setup.py bdist_wheel 1>/dev/null && \
    python setup.py install 1>/dev/null && \
	find . -type f -name "*.pyc" -delete

# a non-sudo user for the app to run on
ARG username=app
RUN adduser -D -u 1000 $username
USER $username
WORKDIR /home/app
RUN which congredi

# This'll expose at build, for example:
# docker build --build-args exposeport=2000
# docker run -d congredi:latest
# should be exposed at 0.0.0.0:2000

# To change the port on a run, open that port with the docker cli.
# docker run -p 1001 -d congredi:latest congredi -p 1001 peer
# should be exposed at 0.0.0.0:1001

ARG exposeport=8800
ENV runport=$exposeport
EXPOSE $exposeport

CMD congredi -p $runport peer
FROM alpine:edge
RUN apk -U add nginx tor supervisor
RUN mkdir /run/nginx
ADD ./nginx.conf /etc/nginx/sites-enabled/default.conf
ADD ./torrc /etc/tor/torrc
ADD ./supervisord.conf /supervisord.conf
CMD supervisord -c /supervisord.conf
