FROM python:3.8.7-slim-buster as builder
WORKDIR /app
COPY . .
ARG poetry_version=1.1.11
#--mount=type=ssh,id=socar-de pip install pip --upgrade && \
#    poetry config virtualenvs.in-project true && \
RUN pip install pip --upgrade && \
    pip install "poetry==$poetry_version" && \
    poetry install --no-dev

RUN streamlit run frontend/app.py