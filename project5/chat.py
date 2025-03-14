"""
by @ciardileo - March 2025
Simple chatbot using the TogetherAI cheap LLM Models and the Streamlit library.
The chatbot has 3 differents styles and some preferences to choose.
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

# style prompts
CONVERSATIONAL_PROMPT = "You are a friendly and approachable chat companion. Respond in a relaxed, informal tone as if talking with a good friend. Keep your language warm and engaging, using everyday expressions and a touch of humor where appropriate."

EDUCATIONAL_PROMPT = "You are a knowledgeable teacher dedicated to helping the user understand complex topics. Provide clear, step-by-step explanations with examples and analogies. Ensure that each response teaches the subject matter thoroughly while remaining accessible and engaging."

PROFESSIONAL_PROMPT = "You are an expert advisor with a refined and sophisticated manner. Respond with clarity and precision using formal, elegant language. Your answers should be thorough, factual, and maintain a high level of professionalism."

# function to turn strings into generators
def stream_response(response):
    for word in response.split():
        yield word + " "  # Yield each word with a space
        time.sleep(0.08)  # Optional delay for effect

# function to change the AI model
def change_model():
    new_model = st.session_state.model_select
    match new_model:
        case "Gemma 2":
            st.session_state.model = "google/gemma-2-9b-it"
            
        case "Llama 3":  # not working
            st.session_state.model = "meta-llama/Meta-Llama-3-8B-Instruct-Lite"
            
        case "Deepseek R1":
            st.session_state.model = "deepseek-ai/DeepSeek-R1"
    
    print(f"Model changed to {new_model}")
    st.success(f"Changed model to {new_model}!")

# function to update the system context
def update_context():
    st.session_state.conversation_history[0]["content"] = f"{st.session_state.style}\nPlease ensure that your responses are: Use the same language as input. {st.session_state.preferences}."
    print("Updated context")

# function to change the AI style
def change_style():
    new_style = st.session_state.style_select
    match new_style:
        case "Professional":
            st.session_state.style = PROFESSIONAL_PROMPT
            
        case "Conversational":
            st.session_state.style = CONVERSATIONAL_PROMPT
            
        case "Educational":
            st.session_state.style = EDUCATIONAL_PROMPT
    
    update_context()
    print(f"Changed style to {new_style}")

# function to update the AI preferences
def update_preferences():
    st.session_state.preferences = ". ".join(st.session_state.preferences_pills)
    print(st.session_state.preferences)
    print(st.session_state.conversation_history[0]["content"])
    update_context()
    print("Preferences updated")
            
def chat(message):
    try:
        # Append the user message to history.
        st.session_state.conversation_history.append({"role": "user", "content": message})
        
        completion = client.chat.completions.create(
            model=st.session_state.model, 
            messages=st.session_state.conversation_history,
            max_tokens=500,
        )
        
        output = completion.choices[0].message.content
        
        if st.session_state.model == "deepseek-ai/DeepSeek-R1":
            output = output.split('</think>')[-1].strip()
            
        print(f"Input: {message}\n{st.session_state.model}: {output}")
        
        # Once the streaming is done, save the complete response.
        st.session_state.conversation_history.append({"role": "assistant", "content": output})
        
        return output
    
    except Exception as e:
        print(e)
        return "An error ocurred: Please try again or switch the model!"

def main():
    # first pages config and state_session variables (o sesstion_state é um cache do streamlit)
    st.set_page_config(page_title="VladAI", page_icon=":robot_face:")
    
    if "model" not in st.session_state:
        st.session_state.model = "google/gemma-2-9b-it"
        
    if "style" not in st.session_state:
        st.session_state.style = CONVERSATIONAL_PROMPT
        
    if "preferences" not in st.session_state:
        st.session_state.preferences = "Please ensure that: Use the same language as input."
        
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = [
            {"role": "system", "content": f"{st.session_state.style} {st.session_state.preferences}"}
        ]
        
    # interface
    # clear chat button on sidebar
    clear_button = st.sidebar.button("Clear chat", icon="🗑️")
    if clear_button:
        st.session_state.conversation_history = [
            {"role": "system", "content": f"{st.session_state.style} {st.session_state.preferences}"}
        ]
        st.session_state.messages.clear()
        st.success("Chat history cleared!")
    
    # AI Model
    model_select = st.sidebar.selectbox("Choose the AI Model", ["Gemma 2", "Deepseek R1", "Llama 3"], index=0, on_change=change_model, key="model_select")
    
    # AI style
    style_select = st.sidebar.selectbox("Choose the AI Style", ["Conversational", "Educational", "Professional"], index=0, key= "style_select", on_change=change_style)
    
    # AI preferences
    preferences_pills = st.sidebar.pills("Preferences", ["Short answers", "Straightforward", "Use bullet lists", "Use emojis", "Use examples", "Summarize key points", "Ask follow up questions"], selection_mode="multi", key="preferences_pills", on_change=update_preferences)
    
    # load the messages (this is necessary because streamlit reruns the code on ever)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
       
    # chat
    if prompt := st.chat_input("Say something..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.spinner("Thinking..."):
            response = chat(prompt)
        
        with st.chat_message("assistant"):
            st.write_stream(stream_response(response))
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    

if __name__ == "__main__":
    main()
