FROM python:3.11

WORKDIR /root
ENV VENV=/opt/venv
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONPATH=/root

RUN apt-get update && apt-get install -y build-essential curl

RUN curl -sSL https://install.python-poetry.org/ | POETRY_VERSION=1.8.0 POETRY_HOME=$HOME/.poetry python \
  && ln -s $HOME/.poetry/bin/poetry /usr/bin/poetry \
  # install dependencies on the python interpreter and not in the poetry virtualenv
  && poetry config virtualenvs.create false

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install --no-interaction --only main

# Copy the actual code
COPY ./peertix_alfred_ai /root/peertix_alfred_ai

# This tag is supplied by the build script and will be used to determine the version
# when registering tasks, workflows, and launch plans
ARG tag
ENV FLYTE_INTERNAL_IMAGE=$tag
