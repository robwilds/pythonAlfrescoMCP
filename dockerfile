# syntax=docker/dockerfile:1

FROM python:3.12.4


WORKDIR /python-docker

COPY . .

RUN apt update && apt-get install nano && rm -rf /var/lib/apt/lists/*

# here need to put the static.json in a temp folder
CMD pip3 install -r requirements.txt --no-cache-dir --break-system-packages; python3 main.py
# need to check to see if static.json exists in static folder...if not copy from temp folder
