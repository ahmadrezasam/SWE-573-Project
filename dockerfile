
FROM python:3.9.2-slim-buster

WORKDIR /app

LABEL maintainer="recipeApp.com"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean

RUN apt-get update && apt-get install -y gdal-bin
# RUN apt-get update \
#     && apt-get install -y binutils libproj-dev gdal-bin

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000