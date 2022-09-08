FROM python:3.8.7-slim-buster as builder
WORKDIR /app
COPY . .
ARG poetry_version=1.1.11
RUN --mount=type=ssh,id=socar-de pip install pip --upgrade
RUN pip install pip --upgrade
RUN pip install "poetry==$poetry_version"
RUN poetry config virtualenvs.in-project true
RUN poetry install

RUN streamlit run frontend/app.py