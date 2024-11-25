FROM python:3.12-alpine as builder


ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN  pip install --upgrade pip setuptools
RUN apk update \
    && apk add gcc musl-dev librdkafka-dev git  libc-dev build-base linux-headers python3-dev libpq-dev

COPY ./requirements.txt /app/requirements.txt
RUN pip wheel --no-cache-dir  --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.12-alpine

RUN apk update \
    && apk add  git librdkafka curl net-tools postgresql-client redis iputils-ping ethtool tcpdump jq

COPY --from=builder /usr/src/app/wheels /wheels

RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

RUN apk del git

COPY ./docker/ /app/docker/
COPY ./docker/entrypoint.sh /app/docker/entrypoint.sh
COPY ./application/ /app/


RUN addgroup --system app  \
    && adduser -S app -G app
RUN chown -R app:app /app
RUN chown -R app:app /run
RUN chmod +x /app/docker/entrypoint.sh
USER app
WORKDIR /app
ENTRYPOINT [ "sh", "/app/docker/entrypoint.sh" ]

USER app
WORKDIR /app
CMD ["/app/docker/entrypoint.sh"]
