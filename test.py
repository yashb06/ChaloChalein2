import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

def test_langchain_groq():
    try:
        llm = ChatGroq(
            api_key=st.secrets["GROQ_API_KEY"],
            model_name="llama-3.3-70b-versatile"
        )
        
        # Create a list of messages directly
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ]
        
        response = llm.invoke(messages)  # Pass the list of messages directly
        
        st.success("✅ Langchain-Groq connection successful!")
        st.write("Response:", response.content)
        
    except Exception as e:
        st.error(f"❌ Langchain-Groq connection failed: {str(e)}")

if __name__ == "__main__":
    st.title("Langchain-Groq Connection Test")
    test_langchain_groq()