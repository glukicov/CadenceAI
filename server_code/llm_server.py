import yaml
from flask import Flask, request, jsonify, Response
from llama_cpp import Llama

config = yaml.safe_load(open("config.yaml"))
APP_NAME = config["app_name"]
BASE_URL = config["base_url"]

app = Flask(APP_NAME)
model = None


def validate_request(data: dict) -> tuple[Response, int]:
    if 'temperature' not in data and 'max_tokens' not in data:
        return jsonify({"error": "Missing required parameters"}), 400


@app.route(rule=BASE_URL, methods=['POST'])
def process_request() -> str:
    try:
        data = request.get_json()
        validate_request(data=data)

        if model is None:
            model = Llama(model_path=M)




