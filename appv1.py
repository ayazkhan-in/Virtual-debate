import streamlit as st
import os
import google.generativeai as genai

# API key
os.environ["GEMINI_API_KEY"] = "AIzaSyB6YzVFIhEyl1zVNv3hyd6g07a0uIjsxzs"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Chat session with no initial history
chat_session = model.start_chat(history=[])

def chat_with_ai(philosopher, message):
    """Generate a response from the AI as the given philosopher."""
    context = f"You are {philosopher}. Debate with the other philosopher on the user's question. Keep your response concise (under 50 words) and related to the what the user asks."
    response = chat_session.send_message(f"{context}\n{message}")
    return response.text.strip()

# UI Elements
st.title("Virtual Debate")

option1 = st.selectbox(
    "Choose the First Person:",
    ["Plato", "Aristotle", "Thomas Hobbes", "Jean-Jacques Rousseau", "Friedrich Nietzsche", "Mahatma Gandhi", "Winston Churchill", "Martin Luther King Jr.", "Malcolm X"],
    key="selectbox_1"
)

option2 = st.selectbox(
    "Choose the Second Person:",
    ["Plato", "Aristotle", "Thomas Hobbes", "Jean-Jacques Rousseau", "Friedrich Nietzsche",  "Mahatma Gandhi", "Winston Churchill", "Martin Luther King Jr.", "Malcolm X"],
    key="selectbox_2"
)

if option1 == option2:
    st.warning("Please choose two different philosophers for the debate.")

if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []

st.write("Ask anything to these philosophers, and they'll debate!")

user_message = st.text_input("You: ")
num_rounds = st.slider("Number of Debate Exchanges:", min_value=1, max_value=10, value=5)

if st.button("Start Debate"):
    if user_message and option1 != option2:
        st.session_state["conversation_history"].append(f"You: {user_message}")

        debate_message = user_message  # Initial question
        for i in range(num_rounds):
            # First Philosopher Responds
            response1 = chat_with_ai(option1, debate_message)
            st.write(f"**{option1}:** {response1}")
            st.session_state["conversation_history"].append(f"{option1}: {response1}")

            # Second Philosopher Responds
            response2 = chat_with_ai(option2, response1)
            st.write(f"**{option2}:** {response2}")
            st.session_state["conversation_history"].append(f"{option2}: {response2}")

            debate_message = response2  # Pass response2 as input for next round

if st.button("Clear Chat History"):
    st.session_state["conversation_history"] = []

st.write("### Conversation History")
for message in st.session_state["conversation_history"]:
    st.write(message)
