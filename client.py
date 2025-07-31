from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession,types
import asyncio
from contextlib import AsyncExitStack

class MCPClient:
    def __init__(self,url):
        self.url = url
        self.stack = AsyncExitStack()
        self._session = None
        
    async def __aenter__(self):
        read,write,_ = await self.stack.enter_async_context(streamablehttp_client(self.url))
        self._session = await self.stack.enter_async_context(ClientSession(read,write))
        await self._session.initialize()
        return self
    async def __aexit__(self, exc_type, exc_value, traceback):
        # await self.session.close()
        await self.stack.aclose()
    
    async def list_tool(self) -> list[types.Tool]:
        return (await self._session.list_tools()).tools
    
    async def call_tool(self,tool_name, *args, **kwargs):
        return await self._session.call_tool(tool_name, *args, **kwargs)
    
    async def resource(self) -> list[types.Resource]:
        result = await self._session.list_resources()
        return result.resources if result else []
async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        tools = await client.list_tool()
        print("Available tools:", tools)
        if tools:
            tool_name = tools[0].name
            result = await client.call_tool(tool_name, "example_arg")
            print(f"Result from {tool_name}:", result)
        resource = await client.resource()
        print("Resource info:", resource)   

if __name__ == "__main__":
    asyncio.run(main())