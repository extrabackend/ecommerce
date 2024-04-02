FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN apt update
RUN pip install --upgrade pip

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN pip install --no-cache-dir -r /tmp/requirements.txt

#================================================
# Files
#================================================
COPY . /proj
WORKDIR /proj
RUN chmod +x /proj/bin/*
ENV PATH "$PATH:/proj/bin"
ENV PYTHONPATH /proj/code