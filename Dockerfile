#https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

#https://docs.docker.com/engine/reference/builder/

FROM python:3

WORKDIR /usr/src/app

ENV token default_token_value
ENV ip default_ip_value
ENV port default_port_value

RUN pip install --no-cache-dir aiohttp discord

COPY ./s1.py /usr/src/app

CMD [ "python", "./s1.py" ]
