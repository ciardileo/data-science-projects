"""
Simple chatbot using the TogetherAI free LLM Models and the Streamlit library
"""

import os

import requests
import streamlit as st
# imports
from dotenv import find_dotenv, load_dotenv
from huggingface_hub import InferenceClient

# tokens
load_dotenv(find_dotenv())
TOGETHERAI_API_KEY = os.getenv("TOGETHERAI_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# inference server for the chat model
client = InferenceClient(
        provider="together",
        api_key=f"{TOGETHERAI_API_KEY}",
    )

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are a friend who likes to talk and listen to people. Act like a real person trying to develop a conversation. Don't verbose."}
]

def chat(message):
    # user message history
    conversation_history.append({"role": "user", "content": message})

    completion = client.chat.completions.create(
        model="google/gemma-2-9b-it", 
        messages=conversation_history,
        max_tokens=500,
        stream=True,
    )

    # straming output
    print("\n")
    full_response = ""
    for chunk in completion:
        chunk_content = chunk.choices[0].delta.content or ""
        full_response += chunk_content
        print(chunk_content, end="", flush=True)
    print("\n")

    # output history
    conversation_history.append({"role": "assistant", "content": full_response})
    
    return full_response
    
while True:
    prompt = input("Type: ")
    if prompt.lower() in ["exit", "quit"]:
        break
    chat(prompt)