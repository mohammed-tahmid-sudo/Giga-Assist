import json
import sqlite3
import os
from fastapi import FastAPI
from openai import OpenAI
from openai.types.responses import response
from pydantic import BaseModel
from typing import Literal
import variables
import init
import classes as c

API_KEY, URL, history, client = init.initialize()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Server_name": "Giga-Assist", "Owner/Developer": "Meee(tahmid)"}


@app.post("/chat/")
def send_message(data: c.SendMessage):
    completion = client.chat.completions.create(
        extra_body={},
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[history, {"role": "user", "content": data.prompt}],
    )
    history["conversations"].append(
        {"role": "user", "content": data.prompt},
    )
    history["conversations"].append(
        {"role": "assistant", "content": completion.choices[0].message.content},
    )
    with open(variables.HISTORY_FILE, "w+") as file:
        json.dump(history, file, indent=4)

    return {"received": completion.choices[0].message.content}


@app.post("/api-key")
def get_api_key(apikey: c.ApiKey):
    data = {
        "api-key": apikey.api_key,
        "server-url": apikey.server_url,
    }
    with open(variables.STORED_DATA, "w") as file:
        json.dump(data, file)

    global client
    client = OpenAI(api_key=apikey.api_key, base_url=apikey.server_url)

    return {"status": "success", "message": "API configuration updated"}


@app.get("/system_prompt")
def set_system_prompt(SendPrompt: c.SendPrompt):
    pass


@app.get("/local-mcp")
def local_mcp(LocalMCP: c.LocalMCP):
    pass


@app.get("/remote-mcp")
def remove_mcp(remoteMCP: c.RemoteMCP):
    pass
