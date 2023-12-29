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

# Copy the docker-entrypoint.sh script to the /src/app directory
COPY docker-entrypoint.sh /src/app/

# Set execute permission for the script
RUN chmod +x /src/app/docker-entrypoint.sh

# Define environment variable
ENV NAME venv

# CMD ["python","manage.py", "runserver"]
CMD [ "./docker-entrypoint.sh" ]