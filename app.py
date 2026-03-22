import streamlit as st
import google.generativeai as genai
import pymongo
import datetime

# 1. Page ki setting
st.set_page_config(page_title="Lucky AI Chatbot", page_icon="🤖")
st.title("🤖 Lucky AI Chatbot")
st.write("Mujhse kuch bhi puchiye!")

# 2. Secrets se Keys lena
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    MONGO_URI = st.secrets["MONGO_URI"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Secrets load karne mein error: {e}")
    st.stop()

# 3. MongoDB se Connect karna 
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(MONGO_URI)

try:
    client = init_connection()
    db = client["ChatbotDB"]           # Database ka naam
    collection = db["UserChats"]       # Table/Collection ka naam
except Exception as e:
    st.error(f"Database se connect nahi ho paya: {e}")

# 4. Model load karna
model = genai.GenerativeModel('gemini-2.5-flash')

# 5. Session state memory UI ke liye
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input aur AI ka Jawab
if prompt := st.chat_input("Aapka sawal yahan likhein..."):
    # User message UI par
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI Response
    with st.spinner("Soch raha hoon..."):
        try:
            response = model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = f"Error aaya: {e}"

    # AI message UI par
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # 💾 7. DATABASE MEIN SAVE KARNA
    chat_document = {
        "timestamp": datetime.datetime.now(),
        "user_message": prompt,
        "ai_reply": reply
    }
    collection.insert_one(chat_document)
