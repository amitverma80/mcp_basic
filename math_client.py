from fastmcp.client import Client
import asyncio
import json
import re
from google import genai


class MCPClient:
    def __init__(self, server_url: str, client: Client, list_tool: None):
        self.server_url = server_url
        self.client = client
        self.tools = list_tool    

    async def process_query(self, query: str) -> str:
        tool_prompt = """
            You are a tool selector. You have access to the following tools: {tools}. 
            A user will provide a query, and you must determine if one of the tools can be used to answer the query.

            Respond ONLY with a JSON object (or an array of JSON objects if multiple tools are needed) that specifies the tool to use and the arguments to pass to the tool. 
            The JSON must be valid and easily parsed by Python's `json.loads()` function. 
            Ensure that the JSON contains no special characters, escape sequences, or unnecessary whitespace that could cause parsing errors. 
            All strings in the JSON must be properly escaped.

            If no tool is appropriate, respond with the JSON value `null`.

            In the json the key for tool name will be tool_code and the key for arguments will be arguments.


            The "tool_code" field should match the name of one of the available tools.
            The "arguments" field should be a JSON object containing the necessary parameters for the tool.
            Now, respond to the following query: {query}
        """
        contents = tool_prompt.format(query=query, tools=self.tools)
        # Initialize Google GenAI client
        gen_client = genai.Client(api_key="<YOUR_API_KEY>")
        response = gen_client.models.generate_content(
            model="gemini-1.5-flash",
            contents=contents,
        )
      
        clean_str = re.sub(
            r"^```json\s*|\s*```$", "", response.text.strip(), flags=re.DOTALL
        )
        data = json.loads(clean_str)
        result = await self.client.call_tool(
            name=data["tool_code"], arguments=data["arguments"]
        )
        return result


async def main():
    server_url = "http://localhost:8000/mcp"
    client = Client(server_url)

    async with client:
        print(f"Connecting to MCP server at {server_url}...")
        print(f"Client connected: {client.is_connected()}")

        tools = await client.list_tools()

        mcp_client = MCPClient(server_url, client, tools)

        query = "What is the addition of 23 and 56.67?"
        print(f"Processing query: {query}")
        result = await mcp_client.process_query(query)
        print(f"Query result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
