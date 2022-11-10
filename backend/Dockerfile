# syntax=docker/dockerfile:1
FROM python:3.10.8-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*
WORKDIR /app/backend
COPY . /app/backend/
RUN pip install -r requirements.txt
