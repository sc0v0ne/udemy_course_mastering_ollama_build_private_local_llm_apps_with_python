import ollama

def ollama_list() -> None:
    response_ollama = ollama.list()
    print('Ollama List')
    print('-'*30)
    models = response_ollama['models']
    for model in models:
        for k, v in model.items():
            print(f'{k}: {v}')

def chat() -> None:
    print('+'*30)
    print('Chat llamma')
    res = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": "why is the ocean so salty ?"
            }
        ],
        stream=True,
    )
    for chunck in res:
        print(chunck["message"]["content"], end="", flush=True)

def main() -> None:
    ollama_list()
    chat()

if __name__ == "__main__":
    main()