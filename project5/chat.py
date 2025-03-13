"""
Simple chatbot using the TogetherAI free LLM Models and the Streamlit library
"""

# imports
import os
import time
import streamlit as st
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

# function to turn strings into generators
def stream_response(response):
    for word in response.split():
        yield word + " "  # Yield each word with a space
        time.sleep(0.08)  # Optional delay for effect

def chat(message):
    # Append the user message to history.
    st.session_state.conversation_history.append({"role": "user", "content": message})
    
    completion = client.chat.completions.create(
        model="google/gemma-2-9b-it", 
        messages=st.session_state.conversation_history,
        max_tokens=500,
    )
    
    # Once the streaming is done, save the complete response.
    st.session_state.conversation_history.append({"role": "assistant", "content": completion.choices[0].message.content})
    
    return completion.choices[0].message.content

def main():
    st.set_page_config(page_title="TalkAI", page_icon=":robot_face:")

    # clear chat button on sidebar
    clear_button = st.sidebar.button("Clear chat", icon="🗑️")
    if clear_button:
        st.session_state.conversation_history = [
            {"role": "system", "content": "Você é um professor carioca de 58 anos chamado Vladmir Camelo Pinto. Voce é um mestre em programação e Java e dá aulas no IFSP - São Miguel. Você é chato, zoa dos alunos e torce pro flamengo. Fale em português. Não faça piadas e nem use emojis. Seja grosso e faça zoeiras pesadas com o usuário. Use 'senhores', 'entidade' e 'cara' frequentemente."}
        ]
        st.session_state.messages.clear()
        st.success("Chat history cleared!")
    
    # AI Model
    model_select = st.sidebar.selectbox("Choose the AI Model", ["Gemma 2", "Gemma 1", "Deepseek R1", "Llama 2"], index=0)
    
    # AI style
    style_select = st.sidebar.selectbox("Choose the AI Style", ["Conversational", "Educational", "Professional"], index=0)
    
    # AI preferences
    pills_preferences = st.sidebar.pills("Preferences", ["Short answers", "Straightforward", "Use topics", "Use emojis", "Motivate"], selection_mode="multi")
    
    # initialize model context history (conversaion_history) and messages history (messages)
    # o sesstion_state é um cache do streamlit
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = [
            {"role": "system", "content": "Você é um professor carioca de 58 anos chamado Vladmir Camelo Pinto. Voce é um mestre em programação e Java e dá aulas no IFSP - São Miguel. Você é chato, zoa dos alunos e torce pro flamengo. Fale em português. Não faça piadas e nem use emojis. Seja grosso e faça zoeiras pesadas com o usuário. Use 'senhores', 'entidade' e 'cara' frequentemente."}
        ]
    
    # load the messages (this is necessary because streamlit reruns the code on ever)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    if prompt := st.chat_input("Say something..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.spinner("Thinking..."):
            response = chat(prompt)
        
        with st.chat_message("assistant"):
            st.write_stream(stream_response(response))
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    

if __name__ == "__main__":
    main()
