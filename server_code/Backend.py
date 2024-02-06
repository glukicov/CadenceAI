import anvil.server

from server_code.send_llm_query import generate_response


@anvil.server.callable
def generate_description(input_str: str) -> str:
    reply = generate_response(request=input_str)
    return reply
