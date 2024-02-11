### Get lightweight Python container
FROM python:3.10-slim

# Author
MAINTAINER Gleb Lukicov <https://glukicov.github.io>

# Add a volume and set as working directory
WORKDIR /api
RUN mkdir -p /api/artifacts

## Copy from local into the container image
COPY ./poetry.lock poetry.lock
COPY ./pyproject.toml pyproject.toml
COPY ./config.yaml config.yaml
COPY ./server_code/llm_server.py /api/llm_server.py
COPY ./artifacts/llama-2-7b-chat.Q2_K.gguf /api/artifacts/llama-2-7b-chat.Q2_K.gguf
#COPY ${MODEL_PATH} /api/${MODEL_PATH} TODO

# Get system updates
RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3-dev gcc libc-dev libffi-dev libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 -y

# Upgrade pip
RUN pip install --upgrade pip

# Install Poetry
RUN pip install "poetry==1.7.1"

# DEV: Poetry venv wit test dependecies
RUN poetry install

# DEV: run a single uvicorn worker with live-reload for code mounted via `volumes` in docker-compose.yml
CMD exec poetry run uvicorn tenyks_mlops.api_service:api --reload --host 0.0.0.0 --port ${PORT}

# expose container port
EXPOSE ${PORT}
