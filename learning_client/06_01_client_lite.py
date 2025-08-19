from mcp import ClientSession
from contextlib import AsyncExitStack
import asyncio
from mcp.client.streamable_http import streamablehttp_client
class MCPClient:
    def __init__(self,url):
        self.session = ClientSession(url)
        self.stack = AsyncExitStack()
        self._sess = None
    async def list_tools(self):
        async with self.session as session:
            response = (await session.list_tools).tools
        return response
    async def __aenter__(self):
        read,write, _ = await self.stack.enter_async_context(streamablehttp_client(self.url))
        self._sess = await self.stack.enter_async_context(ClientSession(read, write))
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.stack.aclose()
async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        tools = await client.list_tools()
        for tool in tools:
            print(f"Tool name: {tool.name}, Description: {tool.description}")

if __name__ == "__main__":
    asyncio.run(main())