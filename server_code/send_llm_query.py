import requests
import json
import argparse
import yaml

from loguru import logger
from llama_cpp import Llama

from server_code.llm_server import (create_llama_prompt, BASE_URL, PORT, MODEL_PATH, API_ENDPOINT)

parser = argparse.ArgumentParser(description="Send a query to the chat completion API.")
parser.add_argument("--question", type=str, required=True, help="The question to ask.")
parser.add_argument("--local_server", action='store_true', help="Send request to a local server")
parser.add_argument("--local_model", action='store_true', help="Send request to a local model")
args = parser.parse_args()

config = yaml.safe_load(open("config.yaml"))
HEADERS = config['headers']
CONTENT = config['content']
TEMPERATURE = config['temperature']
MAX_TOKENS = config['max_tokens']
STREAM = config['stream']


def local_model_response(request: str) -> str:
    model = Llama(model_path=MODEL_PATH)
    prompt = create_llama_prompt(content=CONTENT, user_msg=request)
    output = model(prompt=prompt, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, stream=STREAM)
    return output


def generate_response(request: str) -> str:
    request_data = {
        "messages": [
            {"role": "system", "content": CONTENT},
            {"role": "user", "content": request},
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stream": STREAM,
    }

    json_string = json.dumps(request_data)
    response = requests.post(f"{BASE_URL}:{PORT}{API_ENDPOINT}", headers=HEADERS, data=json_string)
    if response.status_code == 200:
        response_data = response.json()
        for message in response_data["choices"]:
            return message["message"]["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"


if __name__ == "__main__":
    if args.local_model:
        api_response = local_model_response(request=args.question)
    else:
        api_response = generate_response(request=args.question)
    logger.info(api_response)
