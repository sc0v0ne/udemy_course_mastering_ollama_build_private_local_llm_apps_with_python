import ollama

def ollama_show() -> None:
    response_ollama = ollama.generate(
        model="llama3.2",
        prompt="Why is the sky blue ?"
    )
    print(ollama.show("llama3.2"))

def main() -> None:
    ollama_show()

if __name__ == "__main__":
    main()