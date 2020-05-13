FROM python:3.6-slim-buster

RUN apt-get update  && apt-get install -y build-essential
RUN ["pip3", "install", "pipenv"]
ENV PIPENV_VENV_IN_PROJECT 1
WORKDIR /usr/src/app
COPY ./rose_be ./rose_be
COPY ./Pipfile .

RUN ["pipenv", "install"]

COPY ./uWSGI .
EXPOSE 5000
CMD ["pipenv", "run", "uwsgi", "--ini", "app.ini"]
