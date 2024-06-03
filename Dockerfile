# Use the official Python image as the base image
FROM python:3.10-alpine as base

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

RUN set -ex \
    && apk update \
    && apk upgrade \
    # Install build dependencies
    && apk add --no-cache --virtual build-dependencies make g++ postgresql-dev

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/requirements.txt

# Copy certificates to run server with https
COPY cert.pem /app/cert.pem
COPY key.pem /app/key.pem

RUN set -ex && python3 -m venv $VIRTUAL_ENV

# Install the Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory into the container
COPY ./registraai /app/registraai/

# Set the PYTHONPATH to include the /app directory
ENV PYTHONPATH="${PYTHONPATH}:/app/registraai"
ENV PYTHONUNBUFFERED=1

# Specify the command to run when the container starts
CMD ["python", "registraai"]
