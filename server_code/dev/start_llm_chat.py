# Chat with an intelligent assistant in your terminal
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

history = [
    {"role": "system",
     "content": "You are a friendly cycling coach. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user",
     "content": "Hello, I would like to learn how to ride a bike better."},
]

while True:
    completion = client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    print()
    history.append({"role": "user", "content": input("> ")})