# syntax=docker/dockerfile:1
FROM node:17.3.1-alpine3.15
WORKDIR /app/frontend
COPY ./src /app/frontend/src
COPY ./public /app/frontend/public
COPY ./package-lock.json /app/frontend/package-lock.json
COPY ./package.json /app/frontend/package.json
RUN npm ci
