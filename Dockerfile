# TODO: use socar-data image on main build
ARG python_version="3.8"
FROM gcr.io/socar-data-dev/python-${python_version}-slim-buster-git-docker
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
ARG poetry_version=1.1.11
ARG app_home="/app/somlier"
WORKDIR $app_home
COPY . $CWD
WORKDIR $CWD

# 파이썬 패키지 설치
RUN --mount=type=ssh,id=socar-de pip install pip --upgrade && \
    pip install "poetry==$poetry_version" && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev
