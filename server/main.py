from fastapi import FastAPI
from openai.types.responses import response
from pydantic import BaseModel
from typing import Literal
import json
from openai import OpenAI

# data = {"api-key": "NAN"}

with open("data.json", "r") as file:
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
    print("\033[31mClient initialization skipped due to missing credentials.\033[0m")
    client = None

app = FastAPI()


class SendMessage(BaseModel):
    model: str
    prompt: str


class ApiKey(BaseModel):
    server_url: str
    api_key: str


class SendPrompt(BaseModel):
    message: str


class LocalMCP(BaseModel):
    name: str
    transport: Literal["stdio"] = "stdio"
    command: str
    args: list[str] = []
    env: dict[str, str] = {}


class RemoteMCP(BaseModel):
    name: str
    transport: Literal["streamable-http"] = "streamable-http"
    url: str
    headers: dict[str, str] = {}


@app.get("/")
def read_root():
    return {"Server_name": "Giga-Assist", "Owner/Developer": "Meee(tahmid)"}


@app.post("/chat/")
def send_message(data: SendMessage):
    completion = client.chat.completions.create(
        extra_body={},
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[{"role": "user", "content": data.prompt}],
    )
    # print(completion.choices[0].message.content)
    print(completion)

    return {"received": completion.choices[0].message.content}


@app.post("/api-key")
def get_api_key(apikey: ApiKey):
    data = {
        "api-key": apikey.api_key,
        "server-url": apikey.server_url,
    }
    with open("data.json", "w") as file:
        json.dump(data, file)

    global client
    client = OpenAI(api_key=apikey.api_key, base_url=apikey.server_url)

    return {"status": "success", "message": "API configuration updated"}


@app.get("/system_prompt")
def set_system_prompt(SendPrompt: SendPrompt):
    pass


@app.get("/local-mcp")
def local_mcp(LocalMCP: LocalMCP):
    pass


@app.get("/remote-mcp")
def remove_mcp(remoteMCP: RemoteMCP):
    pass
