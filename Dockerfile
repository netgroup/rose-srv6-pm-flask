FROM python:3.6

RUN apt-get update && apt-get install -y python3-dev
RUN ["pip3", "install", "pipenv"]
ENV PIPENV_VENV_IN_PROJECT 1
WORKDIR /usr/src/app
COPY ./rose_be .
COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN ["pipenv", "install"]

COPY ./uWSGI/app.ini .
EXPOSE 5000
CMD ["pipenv", "run", "uwsgi", "--ini", "app.ini"]

