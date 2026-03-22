import streamlit as st
import google.generativeai as genai

# 1. Page ki setting
st.set_page_config(page_title="Lucky AI Chatbot", page_icon="🤖")
st.title("🤖 Lucky AI Chatbot")
st.write("Mujhse kuch bhi puchiye!")

# 2. API Key setup
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except FileNotFoundError:
    st.error("API Key nahi mili! Kripya Streamlit secrets mein GEMINI_API_KEY add karein.")
    st.stop()

# 3. Model load karna
model = genai.GenerativeModel('gemini-2.5-flash')

# 4. Chat history ko session mein save karna taaki refresh hone par chat gayab na ho
if "messages" not in st.session_state:
    st.session_state.messages = []

# Puraani chat history screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User se input lena
if prompt := st.chat_input("Aapka sawal yahan likhein..."):
    # User ka message UI par dikhana aur history mein save karna
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI se response generate karwana
    with st.spinner("Soch raha hoon..."):
        try:
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = f"Error aaya: {e}"

    # AI ka response UI par dikhana aur history mein save karna
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})