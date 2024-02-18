from typing import List, Dict

import keyring
import yaml
import argparse

from loguru import logger
from openai import OpenAI
from openai.types.chat import ChatCompletion

config = yaml.safe_load(open("config.yaml"))

API_KEY = keyring.get_password(service_name='openai', username='api_key')
CHAT_MODEL = config['chat_model']
SYSTEM_CONTENT = config['system_content']
CHAT_TEMPERATURE = config['chat_temperature']
CHAT_MAX_TOKENS = config['chat_max_tokens']
CHAT_TOP_P = config['chat_top_p']
CHAT_FREQUENCY_PENALTY = config['chat_frequency_penalty']
CHAT_PRESENCE_PENALTY = config['chat_presence_penalty']

client = OpenAI(api_key=API_KEY)


def create_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a query to a remote chat completion API.")
    parser.add_argument("--question", type=str, required=True, help="The question to ask.")
    return parser.parse_args()


def create_sys_usr_msg(system_content: str = SYSTEM_CONTENT, user_content: str = None) -> List[Dict]:
    return [
        {
            "role": "system",
            "content": system_content
        },
        {
            "role": "user",
            "content": user_content
        }
    ]


def call_chat_model(user_content: str) -> ChatCompletion:
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=create_sys_usr_msg(user_content=user_content),
        temperature=CHAT_TEMPERATURE,
        max_tokens=CHAT_MAX_TOKENS,
        top_p=CHAT_TOP_P,
        frequency_penalty=CHAT_FREQUENCY_PENALTY,
        presence_penalty=CHAT_PRESENCE_PENALTY
    )
    return response


if __name__ == "__main__":
    args = create_parser()
    api_response = call_chat_model(user_content=args.question)
    logger.info(f"Response: {api_response.choices[0].message.content}")
