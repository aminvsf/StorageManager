FROM python:3.8.13-slim

COPY . /app
WORKDIR /app

RUN python3 -m venv /opt/venv

RUN apt-get update && \
    apt-get install default-libmysqlclient-dev -y && \
    apt-get install gcc -y && \
    pip install pip --upgrade && \
    pip install -r requirements.txt

COPY base_site.html /usr/local/lib/python3.8/site-packages/django/contrib/admin/templates/admin/base_site.html
