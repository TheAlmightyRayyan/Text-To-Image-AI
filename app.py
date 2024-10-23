import streamlit as st
import requests
import io
from PIL import Image

def query_stabilitydiff(payload, headers):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# --- UI Configurations --- #
st.set_page_config(page_title="💬 Chatbot - Text to Image", page_icon="🖼️", layout="wide")
st.markdown("## Text to Image Generator")
st.caption("🚀 A Streamlit text to image bot by Rayyan")

# --- Initialize session state for messages --- #
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What kind of image do you need me to draw? (example: running cat)"}
    ]

# Show previous prompts and results that saved in session
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
    if "image" in message:
        st.chat_message("assistant").image(message["image"], caption=message["prompt"], use_column_width=True)

# User input prompt
prompt = st.chat_input("Type your command here... (e.g., /imagine a sunset over the mountains)")

# Check if the user provided a prompt
if prompt:
    # Automatically add /imagine command if it's not included
    if not prompt.startswith("/imagine"):
        prompt = f"/imagine {prompt}"

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check if Hugging Face Token is provided
    api_key = ""  # Make sure to manage your API keys securely

    # Generate image
    headers = {"Authorization": f"Bearer {api_key}"}

    with st.spinner("Imagining..."):
        # Query Stable Diffusion
        image_bytes = query_stabilitydiff({"inputs": prompt}, headers)

        # Return Image
        image = Image.open(io.BytesIO(image_bytes))
        msg = f'Here is your image related to "{prompt}"'

        # Show Result
        st.session_state.messages.append({"role": "assistant", "content": msg, "prompt": prompt, "image": image})
        st.chat_message("assistant").write(msg)
        st.chat_message("assistant").image(image, caption=prompt, use_column_width=True)

# Custom styling for chat messages
st.markdown(
    """
    <style>
    .stChatMessage-user {
        background-color: #D5DBDB; 
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .stChatMessage-assistant {
        background-color: #E8F8F5; 
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)
