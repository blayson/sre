FROM python:3.7-slim-buster

RUN mkdir /code
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get -y dist-upgrade && apt install -y netcat

# install dependencies
RUN pip install --upgrade pipenv
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN pipenv install --ignore-pipfile --deploy --system
COPY . /code/

ENTRYPOINT ["/code/entrypoint.sh"]
