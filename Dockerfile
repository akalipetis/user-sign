FROM python:3.6

# Allow for PIPENV_ARGS to be supplied as an argument, so that things like --dev can be included
ARG PIPENV_ARGS

# Needed so that logs are immediately flushed to stdout
ENV PYTHONUNBUFFERED=1

# Use /usr/src/app as the working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install dockerize binary, to wait on external services
# https://github.com/jwilder/dockerize
RUN curl -fSslL https://github.com/jwilder/dockerize/releases/download/v0.6.0/dockerize-linux-amd64-v0.6.0.tar.gz | \
    tar xzv -C /usr/local/bin/

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]

# Install pipenv
RUN pip install pipenv==9.0.1

# First, just copy Pipfile and Pipfile.lock to install dependencies for better caching
COPY ./Pipfile ./Pipfile.lock /usr/src/app/
RUN pipenv install --system --deploy ${PIPENV_ARGS}

# Copy the code in the image
COPY ./ /usr/src/app
