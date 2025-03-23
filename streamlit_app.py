import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure the app
st.set_page_config(
    page_title="Mental Health Counseling Assistant",
    page_icon="🧠",
    layout="centered"
)

# API endpoint URL - modify if needed based on your deployment
API_URL = "http://localhost:8000/api/v1/query"

def query_counselor(user_input):
    """Send user query to the API and get response"""
    try:
        response = requests.post(
            API_URL,
            json={"query": user_input},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "response": f"Error: Received status code {response.status_code}",
                "similar_examples": []
            }
    except Exception as e:
        return {
            "response": f"Error connecting to the server: {str(e)}",
            "similar_examples": []
        }

# App title and description
st.title("Mental Health Counseling Assistant")
st.markdown("""
This virtual assistant provides supportive responses for everyday mental health challenges.
Share your thoughts, and I'll do my best to offer helpful guidance.
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # If this is an assistant message with similar examples
        if message["role"] == "assistant" and "examples" in message:
            with st.expander("View similar counseling examples"):
                for i, example in enumerate(message["examples"]):
                    st.markdown(f"**Example {i+1}:**")
                    st.markdown(f"**User Challenge:** {example['context']}")
                    st.markdown(f"**Counseling Response:** {example['response']}")
                    st.markdown(f"**Similarity Score:** {example['similarity_score']:.2f}")
                    st.markdown("---")

# User input
if prompt := st.chat_input("Share what's on your mind..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_response = query_counselor(prompt)
            response_text = full_response.get("response", "Sorry, I couldn't generate a response")
            similar_examples = full_response.get("similar_examples", [])
            
            st.markdown(response_text)
            
            # Store examples to display in expander
            if similar_examples:
                with st.expander("View similar counseling examples"):
                    for i, example in enumerate(similar_examples):
                        st.markdown(f"**Example {i+1}:**")
                        st.markdown(f"**User Challenge:** {example['context']}")
                        st.markdown(f"**Counseling Response:** {example['response']}")
                        st.markdown(f"**Similarity Score:** {example['similarity_score']:.2f}")
                        st.markdown("---")
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response_text,
        "examples": similar_examples
    })

# Add a sidebar with information
with st.sidebar:
    st.title("About")
    st.markdown("""
    This mental health counseling assistant uses AI to provide supportive responses based on counseling examples.
    
    **Important Note:** While this assistant aims to be helpful, it is not a replacement for professional mental health services.
    """)
