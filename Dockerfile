#FROM python:3-slim
FROM python:3.6-slim
MAINTAINER Jae Kyung Lee <jklee@atommerce.com>

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

ENV INSTALL_PATH /wilson
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .

CMD gunicorn -b 0.0.0.0:8000 --worker-class eventlet -w 1 --access-logfile - "wilson.app:create_app()"
