import streamlit as st
import asyncio
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Note: In a real environment, you'd use a community MCP adapter for LangChain.
# For this lab, we mock the tool binding concept to show the architecture.
# We will assume a helper function `get_mcp_tools()` exists that connects
# to server.py and returns LangChain-compatible tools.

st.title("📚 Local MCP Desktop")

# --- UI Sidebar: Model Selection ---
with st.sidebar:
    st.header("Settings")
    model_provider = st.selectbox(
        "Choose Model Provider",
        ("Local (Ollama)", "Anthropic (Claude)")
    )

    if model_provider == "Anthropic (Claude)":
        api_key = st.text_input("Enter Anthropic API Key", type="password")
    else:
        st.info("Ensure Ollama is running locally (e.g., `ollama run llama3`).")

# --- Chat Interface ---
# Initialize stateless history (cleared on refresh)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask about the library database..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Agent Orchestration ---
    with st.chat_message("assistant"):
        st_placeholder = st.empty()
        st_placeholder.markdown("🤔 Thinking...")

        try:
            # 1. Initialize the chosen LLM
            if model_provider == "Local (Ollama)":
                # Connects to a local Ollama instance
                llm = ChatOllama(model="llama3", base_url="http://ollama-service:11434")
            else:
                if not api_key:
                    st.error("Please enter your API Key in the sidebar.")
                    st.stop()
                llm = ChatAnthropic(model="claude-3-haiku-20240307", api_key=api_key)

            # Mocking the response for the UI demonstration
            response_text = f"Using {model_provider}, I would query the database to answer: '{prompt}'"

            # Show final response
            st_placeholder.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            st_placeholder.error(f"Error: {str(e)}")
