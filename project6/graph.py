"""
Following the tutorial: https://www.youtube.com/watch?v=q2XPEjQ4Yt0&list=WL&index=3
"""

# imports
from pydantic import BaseModel
from langchain_ollama import ChatOllama  # biblioteca que permite que o langchain se comunique com modelos locais
from langgraph.graph import START, END, StateGraph
from langgraph.types import Send
from schemas import *
from prompts import *
from dotenv import load_dotenv
import os

# env tokens
load_dotenv()
