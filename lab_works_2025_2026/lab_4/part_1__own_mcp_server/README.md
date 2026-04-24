# How to run the code

# I. Create & validate creation of Postgres database

1. Go to this directory in your console.
2. Run command: `docker compose up -d`
3. Validate with command: `docker exec -e PGPASSWORD='M&1_V3r^_C9#pLeX_P@$s' -it mcp_postgres_db psql -U mcp_user -d mcp_database -c "SELECT * FROM books;"`
4. P.s. without pass it also works: `docker exec -it mcp_postgres_db psql -U mcp_user -d mcp_database -c "SELECT * FROM books;"`,
   but I've kept the pass for possible testings.

# II. Create own MCP server

1. After executing all commands above, and confining that your DB is filled with data go to the directory `mcp_server`
2. Analyze the code in `mcp_server/database.py` -- here is connection to your DB via Python
3. Test if the connection via Python to DB works by executting `./mcp_server/__test__db_conn.py`
4. Analyze the code in `./mcp_server/server.py` -- there is your actual MCP server
5. Check if all works on your "Claude Desktop"
   1. Press `Win + R` to open the Run dialog. 
   2. Type `%APPDATA%\Claude` and press `Enter`. 
   3. Look for a file named `claude_desktop_config.json`.
   4. Add to that file:
```json
{
  "mcpServers": {
    "library-lab-server": {
      "command": "D:\\documents\\python_projects\\Computational_Intelligence_course\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\documents\\python_projects\\Computational_Intelligence_course\\lab_works_2025_2026\\lab_4\\part_1__own_mcp_server\\mcp_server\\server.py"
      ]
    }
  }
}
```
   5. Fully restart your `Claude Desktop`
6. `TODO 1`: your task here is to add a few tool-function to `./mcp_server/server.py` like it was in the example.
7. `TODO 2`: check if your code works using "Claude Desktop" and connect it with your MCP server.

