# Lab 4: Description

## Part I: Develop own MCP server

1. Create Docker container with Postgres database, which contains 1-3 tables.
2. Make connection to that DB via Python (Pydantic / SQLAlchemy / SQLModel).
3. Create via Python scheme to those tables and fill them with some example data.
4. Write an MCP Server with functions (3-10 functions) to interact with that DB.
5. Connect from Anthropic (Claude) model (look if it possible with other providers like Google / OpenAI / Mistral)

## Part II: Develop own MCP client

1. Develop code for MCP client with using LLM by API and (or) LLM hosted locally. 
   (While you can write this from scratch, libraries like LangChain and LlamaIndex already have built-in MCP tool wrappers. 
   This makes it trivial to swap between Anthropic, Google (Gemini), OpenAI, or local models (via Ollama).)
2. Implement it as server hosted on own Docker container.

---

# How to run the code / do the lab work

## I. Create & validate creation of Postgres database

1. Go to the project root directory (`lab_4`) in your console.
2. Run command: `docker compose up -d`
3. Validate with command: 
   `docker exec -e PGPASSWORD='M&1_V3r^_C9#pLeX_P@$s' -it mcp_postgres_db psql -U mcp_user -d mcp_database -c "SELECT * FROM books;"`
4. *Note: without the password flag it also works (`docker exec -it mcp_postgres_db psql -U mcp_user -d mcp_database -c "SELECT * FROM books;"`), but the password flag is kept for automated testing setups.*

## II. Create own MCP server

1. After executing the commands above and confirming that your DB is filled with data, ensure your terminal is in the `lab_4` root directory.
2. Analyze the code in `src/database.py` — here is the connection to your DB via Python.
3. Test if the connection via Python to the DB works by executing: `python -m tests.test_db_conn`
4. Analyze the code in `src/server.py` — there is your actual MCP server.
5. Check if all works on your `Claude Desktop`:
   1. Press `Win + R` to open the Run dialog. 
   2. Type `%APPDATA%\Claude` and press `Enter`. 
   3. Look for a file named `claude_desktop_config.json`.
   4. Add your server configuration to that file (`TODO`: adjust the paths below to match your actual system paths):
    ```json
    {
      "mcpServers": {
        "library-lab-server": {
          "command": "D:\\documents\\python_projects\\Computational_Intelligence_course\\.venv\\Scripts\\python.exe",
          "args": [
            "D:\\documents\\python_projects\\Computational_Intelligence_course\\lab_works_2025_2026\\lab_4\\src\\server.py"
          ]
        }
      }
    }
    ```
   5. Fully restart your `Claude Desktop`.
   6. Open `Claude Desktop` the `library-lab-server` should appear in the list of your `Connectors`. Like it shown on image below
   ![Claude Desktop: Connectors](.\src_readme\1_claude_desktop_connectors.png)
6. `TODO 1`: Your task here is to add a few tool-functions to `src/server.py` like it was in the example.
7. `TODO 2`: Check if your code works using "Claude Desktop" and connect it with your MCP server.
