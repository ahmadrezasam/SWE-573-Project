
    FROM python:3.9.2-slim-buster

    WORKDIR /app

    ENV PYTHONDONTWRITEBYTECODE 1

    ENV PYTHONUNBUFFERED 1

    COPY ./requirements.txt /app/requirements.txt

    RUN pip install -r requirements.txt

    COPY . /app

    CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000