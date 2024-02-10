import json

import yaml
from flask import Flask, request, Response
from llama_cpp import Llama

config = yaml.safe_load(open("config.yaml"))
APP_NAME = config["app_name"]
API_ENDPOINT = config["api_endpoint"]
BASE_URL = config["base_url"]
PORT = config["port"]
MODEL_PATH = config["model_path"]

EXPECTED_PARAMS = ("temperature", "max_tokens", "stream")

app = Flask(APP_NAME)
model = None


def create_llama_prompt(content: str, user_msg: str) -> str:
    """Return system and user messages in Llama prompt format."""
    return f"""
    <s>[INST] <<SYS>>
    {content}
    <</SYS>>
    {user_msg} [/INST]
    """


def validate_request(request_data: dict) -> Response:
    for param in EXPECTED_PARAMS:
        if param not in request_data:
            return app.response_class(response=json.dumps({"error": "Missing required params"}),
                                      status=400,
                                      mimetype='application/json')

        if 'content' not in request_data['messages'][0] or request_data['messages'][1]:
            return app.response_class(response=json.dumps({"error": "Missing message content"}),
                                      status=400,
                                      mimetype='application/json')

    @app.route(rule=API_ENDPOINT, methods=['POST'])
    def process_request() -> Response:
        global model

        try:
            data = request.get_json()
            validate_request(request_data=data)

            if model is None:
                model = Llama(model_path=MODEL_PATH, n_gpu_layers=TODO)

            prompt = create_llama_prompt(content=data['messages'][0]['content'],
                                         user_msg=data['messages'][1]['content'])
            output = model(prompt=prompt,
                           temperature=data['temperature'],
                           max_tokens=data['max_tokens'],
                           stream=data['stream'])

            return app.response_class(response=json.dumps(output),
                                      status=200,
                                      mimetype='application/json')

        except Exception as e:
            return app.response_class(response=json.dumps({"Error": str(e)}),
                                      status=500,
                                      mimetype='application/json')


if __name__ == '__main__':
    app.run(host=BASE_URL, port=PORT, debug=True)
