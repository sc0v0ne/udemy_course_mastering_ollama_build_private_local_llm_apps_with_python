import ollama


class ModelFile:
    def __init__(self, model: str, name_custom: str, system: str, temp: float = 0.1) -> None:
        self.__model = model
        self.__name_custom = name_custom
        self.__system = system
        self.__temp = temp

    @property
    def name_custom(self):
        return self.__name_custom

    def get_description(self):
        return (
            f"FROM {self.__model}\n"
            f"SYSTEM {self.__system}\n"
            f"PARAMETER temperature {self.__temp}\n"
        )


def ollama_list() -> None:
    response_ollama = ollama.list()
    return response_ollama['models']

def ollama_build(custom_config: ModelFile) -> None:
    ollama.create(
        model=custom_config.name_custom,
        modelfile=custom_config.get_description()
    )


def check_custom_model(name_model) -> None:
    models = ollama_list()
    models_names = [model['name'] for model in models]
    if f'{name_model}:latest' in models_names:
        print('Exists')
    else:
        raise Exception('Model does not exists')

def ollama_generate(name_model, prompt) -> None:
    response_ollama = ollama.generate(
        model=name_model,
        prompt=prompt
    )
    print(response_ollama['response'])

def ollama_delete(name_model) -> None:
    ollama.delete(name_model)

def main(custom_config: ModelFile, prompt) -> None:
    ollama_build(custom_config)
    check_custom_model(custom_config.name_custom)
    ollama_generate(custom_config.name_custom, prompt)
    ollama_delete(custom_config.name_custom)

if __name__ == "__main__":
    prompt: str = 'Who is Naruto Uzumaki ?'
    MF: ModelFile = ModelFile(
        model='llama3.2',
        name_custom='xeroxvaldo_sharopildo',
        system='You are very smart assistant who knows everything about Anime',
    )
    main(MF, prompt)