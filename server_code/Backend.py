import anvil.server
import requests
import json

BASE_URL = "http://localhost:1234"
API_ENDPOINT = "/v1/chat/completions"
headers = {"Content-Type": "application/json"}
ai_content = """
You are a friendly cycling coach.
You always provide well-reasoned answers that are both correct and helpful.
"""
ai_temperature = 0.7
max_tokens = -1
stream = False


@anvil.server.callable
def generate_response(request: str) -> str:
    request_data = {
        "messages": [
            {"role": "system", "content": ai_content},
            {"role": "user", "content": request},
        ],
        "temperature": ai_temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }
    json_string = json.dumps(request_data)

    response = requests.get(f"{BASE_URL}{API_ENDPOINT}", headers=headers, data=json_string)

    if response.status_code == 200:
        response_data = response.json()
        for message in response_data["choices"]:
            return message["message"]["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"
