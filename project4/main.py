"""
O langchain é um framework que permite a criação de LLMs, usando modelos pré-existentes. Ele une várias APIs de IAs diferentes, passando suas próprias bases de dados.
O huggingface é uma plataforma de IA que permite o uso e compartilhamento de modelos de IA. A partir dele é possível baixar modelos de graça para rodar na máquina, ou com alguns limites no servidor deles.

Referências:
https://www.youtube.com/watch?v=_j7JEDWuqLE

This simple app uses a Image-to-Text model to understand the image, then a LLM to create a text and finally a text to speech to read the text.
Models used:
Image do Text: salesforce/blip-image-captioning-base (transformers locally)
LLM: google/gemma-2-9b-it (inference API - together AI)
Text to Speech: espnet/kan-bayashi_ljspeech_vits (inference API - HuggingFace)
"""

# imports
from dotenv import load_dotenv, find_dotenv
from transformers import pipeline  # the transformers are used to run the models locally
from huggingface_hub import InferenceClient
import os
import requests
import streamlit as st

# tokens
load_dotenv(find_dotenv())
TOGETHERAI_API_KEY = os.getenv("TOGETHERAI_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# inference server for the chat model
client = InferenceClient(
        provider="together",
        api_key=f"{TOGETHERAI_API_KEY}",
    )

# image to text
def imagetotext(url):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")  # task: image-to-text
    
    text = image_to_text(url)[0]["generated_text"]
    
    print(text)
    return text

# llm turns image description into a text
def generate_story(context):
    messages = [
        {
            "role": "user",
            "content": f"Create a short story based on this scneario: {context}. Do not create titles, just provide the story. The reading time shouldn't pass 30 seconds.",
        }
    ]

    completion = client.chat.completions.create(
        model="google/gemma-2-9b-it", 
        messages=messages, 
        max_tokens=500,
    )

    output = completion.choices[0].message.content
    print(output)
    return output

    # for deepseek:
    # final_story = output.split('</think>')[-1].strip()
    # print(final_story)

# text to speech
def texttospeech(text):
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}

    payloads = {
        "inputs": text,
    }
    
    response = requests.post(API_URL, headers=headers, json=payloads)
    print(response)
    
    with open('output.wav', 'wb') as f:
        f.write(response.content)

# streamlit ui

def main():
    # page congfig
    st.set_page_config(page_title="Storyteller", page_icon=":robot_face:")
    st.header("Turn images into stories")
    st.subheader("Upload an image and let the AI generate a story for you")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        print(uploaded_file)
        bytes_data = uploaded_file.getvalue()
        with open(uploaded_file.name, "wb") as f:
            f.write(bytes_data)

        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

        # prompting the models
        scenario = imagetotext(uploaded_file.name)
        story = generate_story(scenario)
        texttospeech(story)
        
        # loading the respoonses
        with st.expander("scenario"):
            st.write(scenario)
        
        with st.expander("story"):
            st.write(story)

        # shows the output audio
        st.audio("output.wav")
        
        
if __name__ == "__main__":
    main()