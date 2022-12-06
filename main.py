from typing import Optional
from revChatGPT.revChatGPT import Chatbot
from fastapi import FastAPI, Response, status
import json


app = FastAPI()

from pydantic import BaseModel

class Item(BaseModel):
    prompt: str
    conversation_id: Optional[str]
    parent_id: Optional[str]

with open("config.json", "r") as f:
        config = json.load(f)
chatbot = Chatbot(config)
@app.get("/")
async def read_root(body: Item, response: Response):

    if body.parent_id:
        chatbot.parent_id = body.parent_id
    if body.conversation_id:
        chatbot.conversation_id = body.conversation_id
    
    try:
        result = chatbot.get_chat_response(body.prompt, output="text")
        if result:
            return {"response": result}
        else:
            raise Exception("No response")
    except Exception as e:
        chatbot.refresh_session()
        try: 
            result = chatbot.get_chat_response(body.prompt, output="text")
            if result:
                return {"response": result}
            else:
                raise Exception("No response")
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"response": "Error"}
