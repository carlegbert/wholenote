FROM python:3.6-slim
MAINTAINER Carl Egbert <egbertcarl@gmail.com>

RUN apt-get update && apt-get install -qq -y \
    build-essential libpq-dev --no-install-recommends

ENV INSTALL_PATH /fnote
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:9090 --access-logfile - "fnote.app:create_app()"
