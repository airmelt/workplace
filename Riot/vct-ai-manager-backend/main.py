#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: vct-ai-manager API
@file_name: main.py
@project: vct-ai-manager-backend
@version: 1.0
@date: 2024/10/23 22:11
@author: air
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import logging
from dotenv import load_dotenv

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置Azure OpenAI
API_KEY = os.getenv("AZURE_OPENAI_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

if not API_KEY or not ENDPOINT:
    logger.error("Missing Azure OpenAI configuration")
    raise SystemExit("Error: Missing Azure OpenAI configuration in environment variables.")

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        logger.info(f"Received message: {chat_message.message}")

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are a helpful assistant for VCT AI Manager, an esports management simulation game."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": chat_message.message
                        }
                    ]
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }

        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()

        ai_response = response.json()['choices'][0]['message']['content']
        logger.info(f"AI response: {ai_response}")
        return {"message": ai_response}

    except requests.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to communicate with Azure OpenAI")
    except KeyError as ke:
        logger.error(f"Unexpected response format: {str(ke)}")
        raise HTTPException(status_code=500, detail="Unexpected response from Azure OpenAI")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
