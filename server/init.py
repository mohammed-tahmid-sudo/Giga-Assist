import os
from openai import OpenAI
import json 
from variables import *


def initialize():
    os.makedirs("data", exist_ok=True)

    with open(STORED_DATA, "r") as file:
        loaded_data = json.load(file)

    API_KEY = None
    URL = None

    if loaded_data["api-key"] == 0 and loaded_data["server-url"] == 0:
        print("\033[31mAPI KEY AND SERVER NOTFOUND\033[0m")
    else:
        API_KEY = loaded_data["api-key"]
        URL = loaded_data["server-url"]

    if API_KEY and URL:
        client = OpenAI(base_url=URL, api_key=API_KEY)

        print("\033[32mClient initialized successfully!\033[0m")
    else:
        print(
            "\033[31mClient initialization skipped due to missing credentials.\033[0m"
        )
        client = None

    if not os.path.isfile(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump({"conversations": []}, f, indent=4)

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    return [API_KEY, URL, history, client]
