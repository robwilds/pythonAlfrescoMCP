# syntax=docker/dockerfile:1

FROM nginx:latest


WORKDIR /python-docker

COPY . .

RUN apt update && apt-get install -y nano && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt --no-cache-dir --break-system-packages;

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

