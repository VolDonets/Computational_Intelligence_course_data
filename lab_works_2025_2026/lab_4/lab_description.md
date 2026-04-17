# Lab 4: Description

## Part I: Develop own MCP server

1. Create Docker container with Postgres database, which contains 1-3 tables.
2. Make connection to that DB via Python (Pydantic / SQLAlchemy).
3. Create via Python scheme to those tables and fill them with some example data.
4. Write an MCP Server with functions (3-10 functions) to interact with that DB.
5. Connect from Anthropic (Claude) model (look if it possible with other providers like Google / OpenAI / Mistral)

## Part II: Develop own MCP client

1. Develop code for MCP client with using LLM by API and (or) LLM hosted locally. 
   (While you can write this from scratch, libraries like LangChain and LlamaIndex already have built-in MCP tool wrappers. 
   This makes it trivial to swap between Anthropic, Google (Gemini), OpenAI, or local models (via Ollama).))
2. Implement it as server hosted on own Docker container.
