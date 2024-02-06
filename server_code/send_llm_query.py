import requests
import json
import argparse
import yaml

from loguru import logger

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Send a query to the chat completion API.")
parser.add_argument("--question", type=str, required=True, help="The question to ask.")
args = parser.parse_args()

config = yaml.safe_load(open("config.yaml"))

HEADERS = {"Content-Type": "application/json"}
BASE_URL = config['base_url']
API_ENDPOINT = config['api_endpoint']
CONTENT = config['content']
TEMPERATURE = config['temperature']
MAX_TOKENS = config['max_tokens']
STREAM = config['stream']


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
    response = requests.post(f"{BASE_URL}{API_ENDPOINT}", headers=HEADERS, data=json_string)
    if response.status_code == 200:
        response_data = response.json()
        for message in response_data["choices"]:
            return message["message"]["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"


if __name__ == "__main__":
    api_response = generate_response(args.question)
    logger.info(api_response)
