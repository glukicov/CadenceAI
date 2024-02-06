import requests
import json
import argparse

from loguru import logger

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Send a query to the chat completion API.")
parser.add_argument("--question", type=str, required=True, help="The question to ask.")
args = parser.parse_args()

BASE_URL = "http://localhost:1234"
API_ENDPOINT = "/v1/chat/completions"
headers = {"Content-Type": "application/json"}
ai_content = """
You are a friendly cycling coach.
You always provide well-reasoned answers that are both correct and helpful.
"""
temperature = 0.7
max_tokens = -1
stream = False


def generate_response(request: str) -> str:
    request_data = {
        "messages": [
            {"role": "system", "content": ai_content},
            {"role": "user", "content": request},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }

    json_string = json.dumps(request_data)
    response = requests.post(f"{BASE_URL}{API_ENDPOINT}", headers=headers, data=json_string)
    if response.status_code == 200:
        response_data = response.json()
        for message in response_data["choices"]:
            return message["message"]["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"


if __name__ == "__main__":
    api_response = generate_response(args.question)
    logger.info(api_response)
