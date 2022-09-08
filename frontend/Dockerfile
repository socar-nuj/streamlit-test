FROM python:3.8.7-slim-buster as builder
WORKDIR /app
COPY . .
RUN --mount=type=ssh,id=socar-de pip install pip --upgrade && \
    pip install "poetry==$poetry_version" && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev

RUN streamlit run frontend/app.py