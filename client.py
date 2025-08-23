from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession,types
import asyncio
from contextlib import AsyncExitStack
from pydantic import AnyUrl 
from dataclasses import asdict
import json
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
    
    async def list_resource(self) -> list[types.Resource]:
        result = await self._session.list_resources()
        return result.resources if result else []
    async def read_resourse(self, uri:str)->types.ReadResourceResult:
        assert self._session,"Session unavailable, please reset"
        _url = AnyUrl(uri)
        print(f" url = {_url}")
        result = await self._session.read_resource(_url)
        resource = result.contents[0]
        if isinstance(resource,types.TextResourceContents):
            if resource.mimeType == "application/json":
                try:
                    return json.loads(resource.text)
                    
                except json.decoder.JSONDecodeError as e:
                    print(f"JSON ERROR: {e}")
                    
        return resource.text
        
        # print(f"Dictionary of RESULT: {result.__dict__}")
        return result
        
async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        tools = await client.list_tool()
        print(f"Available Tools : {tools}")
        # for tool in tools:
        #     print(f"Availabe tool = {tool.name}")
        # if tools:
        #     for tool in tools:
        #         if tool.name =="read_doc":
        #             result = await client.call_tool(tool.name,)
        #             print(f"Result from {tool}:", result)
        resource = await client.list_resource()
        print("Resource info:", resource)   
        
        read_resource = await client.read_resourse(resource[0].uri)
        # read_resource = await client.read_resourse('docs://documents')
        print("data",read_resource)
        # print(type(read_resource))
        
if __name__ == "__main__":
    asyncio.run(main())