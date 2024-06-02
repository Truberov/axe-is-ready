FROM node:18-alpine
LABEL authors="truberov"

WORKDIR /frontend

COPY package.json package-lock.json ./

RUN npm install

COPY ./ ./

RUN npm run build
