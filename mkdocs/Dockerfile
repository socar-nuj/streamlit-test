FROM python:3.8.7-slim-buster as builder
WORKDIR /app
COPY ./mkdocs/ .
RUN pip install mkdocs-material
RUN mkdocs build

FROM nginx:latest as deploy
COPY --from=builder /app/site /usr/share/nginx/html/
COPY mkdocs/nginx.conf /etc/nginx/conf.d