FROM python:3.10-alpine as development

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
RUN apk add build-base

# Install pip requirements
COPY app/requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

WORKDIR /fastapi_app/app
COPY . /fastapi_app
ENV PYTHONPATH "${PYTHONPATH}:/fastapi_app"

RUN adduser -u 5678 --disabled-password --gecos "" user && chown -R user /fastapi_app
USER user
