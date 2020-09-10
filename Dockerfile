# Multi-stage build

###############################################################################
## Python base image
###############################################################################
FROM python:3.8-slim AS python-base

### Arg
#### See: https://stackoverflow.com/a/56569081
ARG DEBIAN_FRONTEND=noninteractive

### Env
ENV APP_HOST=.
ENV APP_DOCKER=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

### Dependencies
#### System
####  We need libpq-dev in both build and final runtime image
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get -y install libpq-dev \
    && apt-get clean

###############################################################################
## Python builder base image
###############################################################################
FROM python-base AS python-builder-base

### Dependencies
#### System
RUN apt-get -y install gcc python-dev \
    && pip install --upgrade pip

###############################################################################
## Python builder image
###############################################################################

FROM python-builder-base AS python-builder

### Env
ENV PATH=/root/.local/bin:$PATH

### Dependencies
#### Python
COPY ${APP_HOST}/requirements.txt /tmp
RUN pip install --user -r /tmp/requirements.txt

###############################################################################
## App image
###############################################################################
FROM python-base AS app

### Env
ENV PATH=/root/.local/bin:$PATH

### Dependencies
#### Python (copy from python-builder)
COPY --from=python-builder /root/.local /root/.local

### Volumes
WORKDIR ${APP_DOCKER}
RUN mkdir media static logs
VOLUME ["${APP_DOCKER}/media/", "${APP_DOCKER}/logs/"]

# Expose server port
EXPOSE 8000

### Setup app
COPY ${APP_HOST} ${APP_DOCKER}
COPY ${APP_HOST}/contrib/docker/*.sh /
RUN chmod +x /entrypoint.sh \
    && chmod +x /cmd.sh \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

### Run app
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/cmd.sh", "gmmp.wsgi:application"]
