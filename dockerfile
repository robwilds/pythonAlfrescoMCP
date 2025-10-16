# syntax=docker/dockerfile:1

FROM nginx:latest

WORKDIR /python-docker

COPY ./main.py ./server.py ./requirements.txt /python-docker/
COPY ./data/services/wildsalfmcp/nginx.conf /etc/nginx/
COPY ./utils/ /python-docker/utils/
COPY ./tools/ /python-docker/tools/

RUN apt update && apt-get install -y nano && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt --no-cache-dir --break-system-packages;

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chmod +x /python-docker/utils/create_cert.sh
ENTRYPOINT ["/entrypoint.sh"]

