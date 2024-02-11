import argparse
import json
import yaml

from fastapi import FastAPI, Response, Request
from llama_cpp import Llama
from pydantic import BaseModel
from loguru import logger

config = yaml.safe_load(open("config.yaml"))
APP_NAME = config["app_name"]
API_ENDPOINT = config["api_endpoint"]
BASE_URL = config["base_url"]
PORT = config["port"]
MODEL_PATH = config["model_path"]
N_GPU_LAYERS = config['n_gpu_layers']

EXPECTED_PARAMS = ("temperature", "max_tokens", "stream")

api = FastAPI()
model = None


class RequestData(BaseModel):
    system_content: str
    user_content: str
    temperature: float
    max_tokens: int
    stream: bool


def create_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start a Llama server.")
    parser.add_argument("--local_server", action='store_true',
                        help="Send request to a local server")
    return parser.parse_args()


def create_llama_prompt(content: str, user_msg: str) -> str:
    """Return system and user messages in Llama prompt format."""
    return f"""
    <s>[INST] <<SYS>>
    {content}
    <</SYS>>
    {user_msg} [/INST]
    """


@api.get("/")
async def root() -> Response:
    return Response(content=APP_NAME, status_code=200)


@api.get("/health")
async def health_check() -> Response:
    return Response(content=json.dumps({"Status": "OK"}), status_code=200)


@api.post(API_ENDPOINT)
async def process_request(request: Request) -> Response:
    global model
    try:
        request_body = await request.body()
        request_data = RequestData(**json.loads(request_body))
        if model is None:
            model = Llama(model_path=MODEL_PATH, n_gpu_layers=N_GPU_LAYERS)

        prompt = create_llama_prompt(content=request_data.system_content,
                                     user_msg=request_data.user_content)

        output = model(prompt=prompt,
                       temperature=request_data.temperature,
                       max_tokens=request_data.max_tokens,
                       stream=request_data.stream)
        logger.info(f"Output: {output}")
        return Response(content=json.dumps(output), status_code=200)

    except Exception as e:
        return Response(content=json.dumps({"Error": str(e)}), status_code=500)
