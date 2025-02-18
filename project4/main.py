"""
O langchain é um framework que permite a criação de LLMs, usando modelos pré-existentes. Ele une várias APIs de IAs diferentes, passando suas próprias bases de dados.
O huggingface é uma plataforma de IA que permite o uso e compartilhamento de modelos de IA. A partir dele é possível baixar modelos de graça para rodar na máquina, ou com alguns limites no servidor deles.

Referências:
https://www.youtube.com/watch?v=_j7JEDWuqLE

This simple app uses a Image-to-Text model to understand the image, then a LLM to create a text and finally a text to speech to read the text.
"""

# imports
from dotenv import load_dotenv, find_dotenv
from transformers import pipeline  # the transformers are used to run the models locally
import tensorflow as tf

# muting tensorflow logs
import logging
tf.get_logger().setLevel(logging.ERROR)

load_dotenv(find_dotenv())

# image to text
def imagetotext(url):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")  # task: image-to-text
    
    text = image_to_text(url)
    
    print(text)
    return text

imagetotext("https://thumbs.dreamstime.com/b/dois-cachorros-na-floresta-verde-mista-descansam-trilha-parque-amig%C3%A1vel-para-c%C3%A3es-c%C3%A3ozinho-australiano-e-pastor-alem%C3%A3o-adulto-249789194.jpg")