import requests
import json
import argparse
import yaml

from loguru import logger
from llama_cpp import Llama

from server_code.llm_server import (create_llama_prompt, BASE_URL, PORT, MODEL_PATH, API_ENDPOINT)

config = yaml.safe_load(open("config.yaml"))
CONTENT = config['content']
TEMPERATURE = config['temperature']
MAX_TOKENS = config['max_tokens']
STREAM = config['stream']
N_GPU_LAYERS = config['n_gpu_layers']

HEADERS = {'accept': 'application/json'}


def create_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a query to the chat completion API.")
    parser.add_argument("--question", type=str, required=True, help="The question to ask.")
    parser.add_argument("--local_server", action='store_true',
                        help="Send request to a local server")
    parser.add_argument("--local_model", action='store_true', help="Send request to a local model")
    return parser.parse_args()


def local_model_response(request: str) -> str:
    model = Llama(model_path=MODEL_PATH, n_gpu_layers=N_GPU_LAYERS)
    prompt = create_llama_prompt(content=CONTENT, user_msg=request)
    output = model(prompt=prompt, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, stream=STREAM)
    return output


def form_request(request: str) -> dict:
    return {
        "user_content": request,
        "system_content": CONTENT,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stream": STREAM,
    }


def generate_response(request: str,
                      base_url: str = BASE_URL,
                      port: int = PORT,
                      api_endpoint: str = API_ENDPOINT) -> str:
    request_data = form_request(request=request)
    response = requests.post(url=f"{base_url}:{port}{api_endpoint}",
                             headers=HEADERS,
                             json=request_data)

    if response.status_code == 200:
        response_data = response.json()
        print("response_data", response_data)
        for message in response_data["choices"]:
            return message["message"]["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"


if __name__ == "__main__":
    args = create_parser()
    if args.local_model:
        api_response = local_model_response(request=args.question)
    if args.local_server:
        api_response = generate_response(request=args.question, base_url="http://127.0.0.1")
    else:
        api_response = generate_response(request=args.question)
    logger.info(api_response)
