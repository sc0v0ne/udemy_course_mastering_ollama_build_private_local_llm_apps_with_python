import os.path as osp
import ollama as oll


def ollama_list() -> None:
    response_ollama = oll.list()
    return response_ollama['models']


def check_custom_model(name_model) -> None:
    models = ollama_list()
    models_names = [model['name'] for model in models]
    if f'{name_model}:latest' in models_names:
        print('Exists')
    else:
        raise Exception('Model does not exists')

def ollama_generate(name_model, prompt) -> None:
    response_ollama = oll.generate(
        model=name_model,
        prompt=prompt
    )
    return response_ollama.get("response", "")

def main(name_model, prompt, path_out) -> None:

    check_custom_model(name_model)
    cat_txt = ollama_generate(name_model, prompt)

    print("==== Categorized List: ===== \n")
    print(cat_txt)

    with open(path_out, "w") as f:
        f.write(cat_txt.strip())

if __name__ == "__main__":

    path_in: str = osp.join('data', 'grocery_list.txt')
    path_out: str = osp.join('data', 'categorized_grocery_list.txt')

    if not osp.exists(path_in):
        raise Exception(f'Input file "{path_in} not found.')

    with open(path_in, 'r') as f:
        items = f.read().strip()
    name_model: str = 'llama3.2'
    prompt: str = (
            "You are an assistant that categorizes and sorts grocery items.\n"
            "Here is a list of grocery items:\n"
            f"{items}\n"
            f"Please:\n"
            f"1. Categorize these items into appropriate categories such as Produce, Dairy, Meat, Bakery, Beverages, etc.\n"
            f"2. Sort the items alphabetically within each category.\n"
            f"3. Present the categorized list in a clear and organized manner, using bullet points or numbering.\n"
        )

    main(name_model, prompt, path_out)