import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_basic_client():
    # 1. Define the connection to your local server
    server_params = StdioServerParameters(
        command="D:\\documents\\python_projects\\Computational_Intelligence_course\\.venv\\Scripts\\python.exe",
        args=[
            "D:\\documents\\python_projects\\Computational_Intelligence_course\\lab_works_2025_2026\\lab_4\\src\\server.py"]
    )

    print("Starting client and connecting to server...")

    # 2. Establish the transport layer (stdio) and initialize the session
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Successfully connected to Library Server!\n")

            # 3. The Discovery Phase: Ask the server what tools it has
            tools_response = await session.list_tools()
            print("--- Discovered Tools ---")
            for tool in tools_response.tools:
                print(f"Tool Name: {tool.name}")
                print(f"Description: {tool.description}")
                print(f"Schema: {tool.inputSchema}\n")

            # 4. The Execution Phase: Trigger a tool manually
            print("--- Testing 'search_books' Tool ---")
            tool_args = {"title_query": "Foundation"}

            # This simulates what the LLM will eventually ask your client to do
            result = await session.call_tool("search_books", tool_args)

            # Print the text response returned from PostgreSQL via your server
            print(result.content[0].text)


if __name__ == "__main__":
    asyncio.run(run_basic_client())
