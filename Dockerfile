FROM python:3.11-slim

USER root:root
RUN apt update && apt install -y build-essential


WORKDIR /home/app

COPY requirements.txt ./requirements.txt
RUN pip install --user -r ./requirements.txt

COPY --chown=app:app . ./
