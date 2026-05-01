import streamlit as st
import asyncio
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_anthropic import ChatAnthropic
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

# 1. Import your database logic from server.py!
# (This is safe because of your `if __name__ == "__main__":` block in server.py)
from server import search_books, add_new_author


# --- Convert async Database functions to LangChain Tools ---
@tool
def tool_search_books(title_query: str) -> str:
    """Search for books in the library database by their title."""
    # Streamlit runs synchronously, so we use asyncio to run your async DB function
    return asyncio.run(search_books(title_query))


@tool
def tool_add_new_author(name: str, nationality: str = None) -> str:
    """Adds a new author to the library database. Always use this before adding a book if the author is new."""
    return asyncio.run(add_new_author(name, nationality))


# Package them up for the LLM
my_tools = [tool_search_books, tool_add_new_author]

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
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask about the library database..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- THE AGENTIC ORCHESTRATION LOOP ---
    with st.chat_message("assistant"):
        st_placeholder = st.empty()
        st_placeholder.markdown("🤔 Thinking...")

        try:
            # Step 1: Initialize LLM
            if model_provider == "Local (Ollama)":
                llm = ChatOllama(model="llama3.1", base_url="http://ollama-service:11434")
            else:
                if not api_key:
                    st.error("Please enter your API Key in the sidebar.")
                    st.stop()
                llm = ChatAnthropic(model="claude-3-haiku-20240307", api_key=api_key)

            # Step 2: Bind the tools to the brain
            llm_with_tools = llm.bind_tools(my_tools)

            # Start the conversation context
            conversation_history = [HumanMessage(content=prompt)]

            # Step 3: Ask the LLM what it wants to do
            ai_msg = llm_with_tools.invoke(conversation_history)
            conversation_history.append(ai_msg)

            # Step 4: Check if the LLM decided to use a database tool!
            if ai_msg.tool_calls:
                st_placeholder.markdown("🛠️ Querying the database...")

                # Execute each tool the LLM asked for
                for tool_call in ai_msg.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]

                    # Route to the correct Python function
                    if tool_name == "tool_search_books":
                        result = tool_search_books.invoke(tool_args)
                    elif tool_name == "tool_add_new_author":
                        result = tool_add_new_author.invoke(tool_args)
                    else:
                        result = "Error: Tool not found."

                    # Add the raw database text back to the conversation history
                    conversation_history.append(
                        ToolMessage(content=str(result), tool_call_id=tool_call["id"])
                    )

                # Step 5: Ask the LLM to read the DB results and formulate a human-friendly answer
                st_placeholder.markdown("🧠 Reading database results...")
                final_ai_msg = llm.invoke(conversation_history)
                response_text = final_ai_msg.content
            else:
                # The LLM didn't need a tool (just regular chatting)
                response_text = ai_msg.content

            # Show final response
            st_placeholder.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            st_placeholder.error(f"Error: {repr(e)}")
