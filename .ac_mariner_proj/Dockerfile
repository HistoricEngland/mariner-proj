FROM python:3.11.8
USER root

## Build Args
ARG PROJ_NAME=project
ARG ARCHES_PATH=./arches
ARG DOCKER_PATH=./docker

## The Args below are only needed if you want to mount the mariner_app, arches_he_sysref_funcs, and arches_he_data_transformation for development/debugging
# ARG MARINER_APP_PATH=./mariner_app
# ARG ARCHES_HE_SYSREF_FUNCS_PATH=./arches_he_sysref_funcs
# ARG ARCHES_HE_DATA_TRANSFORMATION_PATH=./arches_he_data_transformation

## Setting default environment variables
ENV ARCHES_PROJECT=$PROJ_NAME
ENV WEB_ROOT=/web_root
ENV APP_ROOT=${WEB_ROOT}/${ARCHES_PROJECT}
ENV PKG_ROOT=${APP_ROOT}_package
ENV DATA_ROOT=${APP_ROOT}_data
# Root project folder
ENV ARCHES_ROOT=${WEB_ROOT}/arches
ENV WHEELS=/wheels
ENV PYTHONUNBUFFERED=1
ENV NODE_VERSION 20.14.0

RUN apt-get update && apt-get install -y make software-properties-common

# Get the pre-built python wheels from the build environment
RUN mkdir ${WEB_ROOT}
RUN mkdir ${PKG_ROOT}
RUN mkdir ${DATA_ROOT}

# Install packages required to run Arches
# Note that the ubuntu/debian package for libgdal1-dev pulls in libgdal1i, which is built
# with everything enabled, and so, it has a huge amount of dependancies (everything that GDAL
# support, directly and indirectly pulling in mysql-common, odbc, jp2, perl! ... )
# a minimised build of GDAL could remove several hundred MB from the container layer.
RUN apt-get install -y --no-install-recommends curl \
  && apt-get update -y 

RUN curl -sL https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
  && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
  && apt-get update -y 

RUN set -ex \
  && RUN_DEPS=" \
  build-essential \
  mime-support \
  libgdal-dev \
  postgresql-client-14 \
  dos2unix \
  " \
  && apt-get install -y --no-install-recommends $RUN_DEPS


# nvm environment variables
ENV NVM_DIR /usr/local/nvm
RUN mkdir $NVM_DIR



# install nvm
# https://github.com/nvm-sh/nvm#install-script
RUN curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash -

# install node and npm
RUN echo "source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default" | bash -

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN apt install wait-for-it

RUN rm -rf /root/.cache/pip/*

# Install the Arches application
# FIXME: ADD from github repository instead?
COPY $ARCHES_PATH ${ARCHES_ROOT}
RUN chmod +x ${ARCHES_ROOT}/arches/install/arches_admin.py

RUN pip install --upgrade pip setuptools wheel

# Install the project
COPY ./${PROJ_NAME} ${APP_ROOT}
WORKDIR ${APP_ROOT}
RUN pip install -e '.[dev]'


## Install sections below are only needed if you want to mount the mariner_app and arches_he_sysref_funcs for development/debugging

# Install the mariner_app package in editable mode
#ENV MARINER_APP=${WEB_ROOT}/mariner_app
#COPY $MARINER_APP_PATH ${MARINER_APP}
#WORKDIR ${MARINER_APP}
#RUN pip install -e '.[dev]'

# Install the arches_he_sysref_funcs package in editable mode
#ENV ARCHES_HE_SYSREF_FUNCS=${WEB_ROOT}/arches_he_sysref_funcs
#COPY $ARCHES_HE_SYSREF_FUNCS_PATH ${ARCHES_HE_SYSREF_FUNCS}
#WORKDIR ${ARCHES_HE_SYSREF_FUNCS}
#RUN pip install -e '.[dev]'

# Install the arches_he_data_transformation package in editable mode
#ENV ARCHES_HE_DATA_TRANSFORMATION=${WEB_ROOT}/arches_he_data_transformation
#COPY $ARCHES_HE_DATA_TRANSFORMATION_PATH ${ARCHES_HE_DATA_TRANSFORMATION}
#WORKDIR ${ARCHES_HE_DATA_TRANSFORMATION}
#RUN pip install -e '.[dev]'

# From here, run commands from ARCHES_ROOT
WORKDIR ${ARCHES_ROOT}

# Install the local editable Arches to override the installed package - this is so we can debug Arches
RUN pip install -e '.[dev]'
RUN pre-commit install


COPY $DOCKER_PATH/entrypoint.sh /entrypoint.sh
RUN chmod -R 700 /entrypoint.sh && \
  dos2unix /entrypoint.sh

WORKDIR ${WEB_ROOT}
RUN mkdir docker
COPY $DOCKER_PATH/settings_local.py ${WEB_ROOT}/docker/settings_local.py
COPY $DOCKER_PATH/conf.d ${WEB_ROOT}/docker/conf.d
COPY $DOCKER_PATH/supervisor.conf ${WEB_ROOT}/docker/supervisor.conf

RUN pip install supervisor
RUN mkdir /var/log/supervisor
RUN mkdir /var/log/celery

# Set default workdir
WORKDIR ${WEB_ROOT}

# # Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run_arches"]

# Expose port 8000
EXPOSE 8000