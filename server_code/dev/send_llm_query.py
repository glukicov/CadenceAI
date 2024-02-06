import requests
import json
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Send a query to the chat completions API.")
parser.add_argument("--question", type=str, required=True, help="The question to ask the API.")
args = parser.parse_args()

# Define base URL and API endpoint
BASE_URL = "http://localhost:1234"
API_ENDPOINT = "/v1/chat/completions"

# Define request headers
headers = {"Content-Type": "application/json"}

# Define request data with user question from argument
request_data = {
   "messages": [
       {
           "role": "system",
           "content": "You are a friendly cycling coach. You always provide well-reasoned answers that are both correct and helpful.",
       },
       {
           "role": "user",
           "content": args.question,  # Use the question from the argument
       },
   ],
   "temperature": 0.7,
   "max_tokens": -1,
   "stream": False,
}

# Convert request data to JSON string
json_string = json.dumps(request_data)

# Send the POST request with headers and data
response = requests.post(
   f"{BASE_URL}{API_ENDPOINT}", headers=headers, data=json_string
)

# Check for successful response
if response.status_code == 200:
   # Parse the JSON response
   response_data = response.json()

   # Access and print the generated text
   for message in response_data["choices"]:
       print(message["message"]["content"])
else:
   print(f"Error: API request failed with status code {response.status_code}")
