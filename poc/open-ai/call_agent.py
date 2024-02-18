import time
import keyring
import yaml
import argparse

import numpy as np

from loguru import logger
from openai import OpenAI
from openai.types.chat import ChatCompletion
import matplotlib.pyplot as plt
from typing import List, Dict

config = yaml.safe_load(open("config.yaml"))

API_KEY = keyring.get_password(service_name='openai', username='api_key')
CHAT_MODEL = config['chat_model']
SYSTEM_CONTENT = config['chat_content']
CHAT_TEMPERATURE = config['chat_temperature']
CHAT_MAX_TOKENS = config['chat_max_tokens']
CHAT_TOP_P = config['chat_top_p']
CHAT_FREQUENCY_PENALTY = config['chat_frequency_penalty']
CHAT_PRESENCE_PENALTY = config['chat_presence_penalty']

client = OpenAI(api_key=API_KEY)


def create_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a query to a remote chat completion API.")
    parser.add_argument("--question", type=str, required=True, help="The question to ask.")
    parser.add_argument("--profile", action='store_true', help="Flag to run a profiler.")
    return parser.parse_args()


def create_sys_usr_msg(system_content: str = SYSTEM_CONTENT, user_content: str = None) -> List[
    Dict]:
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


def make_plot(t: List[float]) -> None:
    mean = np.mean(t)
    std = np.std(t)
    p50 = np.percentile(t, 50)
    p95 = np.percentile(t, 95)
    p99 = np.percentile(t, 99)

    plt.hist(t, colour="black")
    plt.xlabel("Request Time [s]")
    plt.ylabel("Count")
    plt.title(f'Model: {CHAT_MODEL[0:10]}, Content: {SYSTEM_CONTENT[0:5]}, \n'
              f'Mean: {mean:.2f} s, Std: {std:.2f} s, \n'
              f'p50: {p50:.2f} s, p95: {p95:.2f} s, p99: {p99:.2f} s')
    name = f"{CHAT_MODEL[0:10]}+{SYSTEM_CONTENT[0:5]}".lower().replace(" ", "_")
    plt.savefig(f"docs/plots/{name}.png")


if __name__ == "__main__":
    args = create_parser()
    if not args.profile:
        api_response = call_chat_model(user_content=args.question)
        logger.info(f"Response: {api_response.choices[0].message.content}")
    if args.profile:
        request_times = []
        for _ in range(10):
            start = time.perf_counter()
            call_chat_model(user_content=args.question)
            request_times.append(time.perf_counter() - start)
        make_plot(t=request_times)
