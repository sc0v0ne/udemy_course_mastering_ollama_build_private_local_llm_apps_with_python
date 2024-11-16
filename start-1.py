import json
import requests

URL: str = "http://localhost:11434/api/generate"

data: dict = {
    "model": "llama3.2",
    "prompt": "Tell me a short story and make it funny.",
}

response_api = (
    requests
    .post(
        URL,
        json=data,
        stream=True
        )
    )


if response_api.status_code == 200:
    print('Generated Text: ', end= ' ', flush=True)

    for line in response_api.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            result = json.loads(decoded_line)

            generated_text = result.get("response", "")
            print(generated_text, end="", flush=True)

else:
    print('Error:', response_api.status_code, response_api.text)