# pull official base image
FROM python:3.8

# set work directory
WORKDIR /src/app

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --upgrade gevent 

# copy project
COPY . .

CMD [ "./docker-entrypoint.sh" ]