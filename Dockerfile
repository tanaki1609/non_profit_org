# pull official base image
FROM python:3.8.3-alpine
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN pip install --upgrade pip
RUN apk add zlib-dev jpeg-dev gcc musl-dev
COPY ./req.txt .
RUN pip install -r req.txt
# copy project
COPY . .