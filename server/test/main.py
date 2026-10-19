import json
import requests

# The base URL of your running FastAPI application
BASE_URL = "http://127.0.0.1:8000"


def test_update_config(api_key: str, server_url: str):
    """Sends a POST request to update the backend OpenAI client credentials."""
    endpoint = f"{BASE_URL}/api-key"
    payload = {"api_key": api_key, "server_url": server_url}

    print(f"Sending configuration to {endpoint}...")

    try:
        response = requests.post(endpoint, json=payload)

        # Print formatting based on success/failure status codes
        if response.status_code == 200:
            print(f"\033[32mSuccess ({response.status_code}):")
            print(json.dumps(response.json(), indent=4))
            print("\033[0m")
        else:
            print(f"\033[31mFailed ({response.status_code}):")
            print(response.text)
            print("\033[0m")

    except requests.exceptions.ConnectionError:
        print(
            "\033[31mError: Could not connect to FastAPI server. Is uvicorn running?\033[0m"
        )


def run_integration_test():
    # ==========================================
    # STEP 1: CONFIGURE YOUR API TESTING TARGET
    # ==========================================
    # Example using OpenRouter Free tier.
    # Swap out variables here to test Groq or FreeLLMAPI.
    # PROVIDER_URL = "https://openrouter.ai"
    # PROVIDER_KEY = "your-openrouter-free-key-here"
    TARGET_MODEL = "meta-llama/llama-3.1-8b-instruct:free"

    # ==========================================
    # STEP 2: TEST THE /api-key ENDPOINT
    # ==========================================
    # config_url = f"{BASE_URL}/api-key"
    # config_payload = {"api_key": PROVIDER_KEY, "server_url": PROVIDER_URL}
    #
    # print(f"1. Sending configuration to {config_url}...")
    # try:
    #     config_res = requests.post(config_url, json=config_payload)
    #     if config_res.status_code == 200:
    #         print(f"\033[32m[PASS] Configuration updated: {config_res.json()}\033[0m\n")
    #     else:
    #         print(
    #             f"\033[31m[FAIL] Config route returned {config_res.status_code}: {config_res.text}\033[0m"
    #         )
    #         return
    # except requests.exceptions.ConnectionError:
    #     print("\033[31m[ERROR] Server offline. Make sure uvicorn is running!\033[0m")
    #     return

    # ==========================================
    # STEP 3: TEST THE /chat/ ENDPOINT
    # ==========================================
    while True:
        chat_url = f"{BASE_URL}/chat/"
        inp = input("ENDTER YOUR PROMPT: ")
        chat_payload = {
            "model": TARGET_MODEL,
            "prompt": inp,
        }

        print(f"2. Sending chat prompt to {chat_url} using model '{TARGET_MODEL}'...")
        chat_res = requests.post(chat_url, json=chat_payload)

        if chat_res.status_code == 200:
            print(f"\033[32m[PASS] Chat Endpoint responded successfully!\033[0m")
            print(json.dumps(chat_res.json(), indent=4))
        else:
            print(
                f"\033[31m[FAIL] Chat failed with code {chat_res.status_code}: {chat_res.text}\033[0m"
            )



if __name__ == "__main__":
    run_integration_test()
