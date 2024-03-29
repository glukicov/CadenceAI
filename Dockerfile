### Get lightweight Python container
FROM python:3.10-slim

# Author
MAINTAINER Gleb Lukicov <https://glukicov.github.io>

# Get system updates
RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3-dev build-essential gcc clang clang-tools cmake libc-dev libffi-dev libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 -y

# Upgrade pip and poetry
RUN pip install --upgrade pip
#RUN pip install "poetry==1.7.1"

# TODO
## Add a volume and set as working directory
#WORKDIR /api
#
### Copy poetry files and appplication files
#COPY ./poetry.lock ./poetry.lock
#COPY ./pyproject.toml ./pyproject.toml
#COPY ./README.md ./README.md
#COPY ./server_code/llm_server.py ./sever_code/llm_server.py
# Copy misc files
#COPY ./config.yaml ./config.yaml
#COPY ./artifacts/llama-2-7b-chat.Q2_K.gguf /api/artifacts/llama-2-7b-chat.Q2_K.gguf

# TODO
COPY . ./

# DEV: Poetry venv wit test dependecies TODO
#RUN poetry install
RUN pip install fastapi uvicorn llama-cpp-python loguru pydantic pyyaml

# DEV: run a single uvicorn worker with live-reload for code mounted via `volumes` in docker-compose.yml
CMD exec uvicorn server_code.llm_server:api --reload --host 0.0.0.0 --port 8080

# expose container port
EXPOSE 8080
