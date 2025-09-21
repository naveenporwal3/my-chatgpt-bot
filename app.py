import streamlit as st
import openai

# -------------------------
# OpenAI API Key
# -------------------------
# Access key from Streamlit secrets (section: general)
openai.api_key = st.secrets["general"]["OPENAI_API_KEY"]

# -------------------------
# App Title
# -------------------------
st.title("💬 My ChatGPT Chatbot")

# -------------------------
# Initialize session state for messages
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# User input
# -------------------------
user_input = st.text_input("Type your message here:")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # System prompt (optional branding / instructions)
    system_prompt = {"role": "system", "content": "You are a helpful assistant."}
    messages = [system_prompt] + st.session_state.messages

    try:
        # Get response from OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        bot_message = response.choices[0].message.content

        # Save bot message
        st.session_state.messages.append({"role": "assistant", "content": bot_message})
    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------
# Display chat history with simple styling
# -------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div style="background-color:#DCF8C6; padding:8px; border-radius:10px; margin:5px 0;"><b>You:</b> {msg["content"]}</div>',
            unsafe_allow_html=True
        )
    elif msg["role"] == "assistant":
        st.markdown(
            f'<div style="background-color:#F1F0F0; padding:8px; border-radius:10px; margin:5px 0;"><b>Bot:</b> {msg["content"]}</div>',
            unsafe_allow_html=True
        )
