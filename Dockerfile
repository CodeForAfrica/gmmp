FROM python:3.7
ENV DEBIAN_FRONTEND noninteractive

# Set env variables used in this Dockerfile
# Local directory with project source
ENV APP_SRC=.
# Directory in container for all project files
ENV APP_SRVHOME=/src
# Directory in container for project source files
ENV APP_SRVPROJ=/src/gmmp

# Create application subdirectories
WORKDIR $APP_SRVHOME
RUN mkdir media static staticfiles logs
VOLUME ["$APP_SRVHOME/media/", "$APP_SRVHOME/logs/"]

# Install requirements
RUN apt-get -qq update \
    && apt-get -qq install -y --no-install-recommends \
        apt-utils \
        postgresql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add application source code to SRCDIR
ADD $APP_SRC $APP_SRVPROJ
WORKDIR $APP_SRVPROJ

RUN pip install -q -r requirements.txt


# Expose port server
EXPOSE 8000

COPY ./contrib/docker/entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD [ "--name", "gmmp", "--reload", "gmmp.wsgi:application"]
