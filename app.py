import streamlit as st
from rag_pipeline import ask_question
import re   # 🔥 ADDED (for formatting)

st.set_page_config(page_title="AI Business Advisor", layout="wide")

st.title("AI Business Advisor")

# 🔥 ADDED FUNCTION (FORMATTER)
def format_output(text):
    text = text.replace("\n", " ")   # clean messy newlines
    
    parts = re.split(r'•|\d+\.', text)   # split bullets/numbers
    
    cleaned = [p.strip() for p in parts if len(p.strip()) > 10]
    
    return "\n\n".join([f"{i+1}. {item}" for i, item in enumerate(cleaned)])


# memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input
user_input = st.chat_input("Ask your business question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    response = ask_question(user_input)

    # 🔥 UPDATED THIS PART (REPLACED OLD FORMAT)
    formatted = format_output(response)

    st.session_state.messages.append({"role": "assistant", "content": formatted})
    

    with st.chat_message("assistant"):
        st.write(formatted)