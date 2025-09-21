import streamlit as st
import openai

# -------------------------
# OpenAI API Key
# -------------------------
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

if user_input.strip():  # Ignore empty inputs
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare system prompt + conversation
    system_prompt = {"role": "system", "content": "You are a helpful assistant."}
    messages = [system_prompt] + st.session_state.messages

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Check if API returned a valid response
        if response.choices and len(response.choices) > 0:
            bot_message = response.choices[0].message.content
        else:
            bot_message = "Sorry, I couldn't generate a response. Please try again."

    except openai.error.RateLimitError:
        bot_message = "Quota exceeded. Please wait and try again later."
    except openai.error.AuthenticationError:
        bot_message = "Invalid API key. Please check your OpenAI key in Streamlit secrets."
    except Exception as e:
        bot_message = f"Error: {e}"

    # Save bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_message})

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
