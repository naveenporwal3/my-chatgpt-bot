import streamlit as st
import openai

# -------------------------
# OpenAI API Key
# -------------------------
# We'll set it in Streamlit secrets later
openai.api_key = st.secrets["OPENAI_API_KEY"]

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

    # Get response from OpenAI GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    bot_message = response.choices[0].message.content

    # Save bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_message})

# -------------------------
# Display chat history
# -------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
