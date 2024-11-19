import os
import json
import asyncio
import random
from ollama import AsyncClient


def load_grocery_list(file_path) -> list:
    if not os.path.exists(file_path):
        print(f'File {file_path} does not exist.')
        return []
    with open(file_path, 'r') as f:
        items = [line.strip() for line in f if line.strip()]
    return items

async def fetch_price_and_nutrition(item) -> None:
    print(f'Fetching price and nutrition data for "item"...')
    
    await asyncio.sleep(0.1)
    return {
        'item': item,
        'price': f'${random.uniform(1, 10):.2f}',
        'calories': f'{random.randint(50, 500)} kcal',
        'fat': f'{random.randint(1, 20)} g',
        'protein': f'{random.randint(1, 30)} g'
    }


async def fetch_recipe(category):
    print(f'Fetching a recipe for the "{category}" category...')
    
    await asyncio.sleep(0.1)
    return {
        "category": category,
        "recipe": f"Delicious {category} dish",
        "ingredients": ["Ingredient 1", "Ingriend 2", "Ingredient 3"],
        "instructions": 'Mix ingredients and cook'
    }


async def main():
    path = os.path.join('data', 'grocery_list.txt')

    g_items = load_grocery_list(path)
    if not g_items:
        print('Grocery list is empty or file not found.')
        return


    client = AsyncClient()

    tools = [
        {
            "type": "function",
            "function": {
                "name": "fetch_price_and_nutrition",
                "description": "Fetch price and nutrition data for a grocery item",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item": {
                            "type": "string",
                            "description": "The name of the grocery item",
                        },
                    },
                    "required": ["item"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "fetch_recipe",
                "description": "Fetch a recipe based on a category",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "The category of food (e.g., Produce, Dairy)",
                        },
                    },
                    "required": ["category"],
                },
            },
        },
    ]

    categorize_prompt = f"""
    You are an assistant that categorizes grocery items.

    **Instructions:**

    - Return the result **only** as a valid JSON object.
    - Do **not** include any explanations, greetings, or additional text.
    - Use double quotes (`"`) for all strings.
    - Ensure the JSON is properly formatted.
    - The JSON should have categories as keys and lists of items as values.

    **Example Format:**

    {{
    "Produce": ["Apples", "Bananas"],
    "Dairy": ["Milk", "Cheese"]
    }}

    **Grocery Items:**

    {', '.join(g_items)}
    """

    messages = [{"role": "user", "content": categorize_prompt}]
    response = await client.chat(
        model="llama3.2",
        messages=messages,
        tools=tools,
    )

    messages.append(response["message"])
    print(response["message"]["content"])

    assistant_message = response["message"]["content"]

    try:
        categorized_items = json.loads(assistant_message)
        print("Categorized items:")
        print(categorized_items)

    except json.JSONDecodeError:
        print("Failed to parse the model's response as JSON.")
        print("Model's response:")
        print(assistant_message)
        return

    fetch_prompt = """
    For each item in the grocery list, use the 'fetch_price_and_nutrition' function to get its price and nutrition data.
    """

    messages.append({"role": "user", "content": fetch_prompt})

    response = await client.chat(
        model="llama3.2",
        messages=messages,
        tools=tools,
    )
    messages.append(response["message"])

    if response["message"].get("tool_calls"):
        print("Function calls made by the model:")
        available_functions = {
            "fetch_price_and_nutrition": fetch_price_and_nutrition,
        }
        item_details = []
        for tool_call in response["message"]["tool_calls"]:
            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]
            function_to_call = available_functions.get(function_name)
            if function_to_call:
                result = await function_to_call(**arguments)
                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(result),
                    }
                )
                item_details.append(result)

                print(item_details)
    else:
        print(
            "The model didn't make any function calls for fetching price and nutrition data."
        )
        return

    random_category = random.choice(list(categorized_items.keys()))
    recipe_prompt = f"""
    Fetch a recipe for the '{random_category}' category using the 'fetch_recipe' function.
    """
    messages.append({"role": "user", "content": recipe_prompt})

    response = await client.chat(
        model="llama3.2",
        messages=messages,
        tools=tools,
    )

    messages.append(response["message"])
    if response["message"].get("tool_calls"):
        available_functions = {
            "fetch_recipe": fetch_recipe,
        }
        for tool_call in response["message"]["tool_calls"]:
            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]
            function_to_call = available_functions.get(function_name)
            if function_to_call:
                result = await function_to_call(**arguments)
                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(result),
                    }
                )
    else:
        print("The model didn't make any function calls for fetching a recipe.")
        return

    final_response = await client.chat(
        model="llama3.2",
        messages=messages,
        tools=tools,
    )

    print("\nAssistant's Final Response:")
    print(final_response["message"]["content"])

    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())