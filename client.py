from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession,types
import asyncio
from contextlib import AsyncExitStack
from pydantic import AnyUrl 
from dataclasses import asdict
import json
from typing import Any
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
    async def list_prompts(self) -> list[types.Prompt]:
        prompts = (await self._session.list_prompts()) 
        return prompts.prompts if prompts else []
    async def read_prompts(self,name:str,arguments:dict[str,str]) -> list[types.GetPromptResult]:
        prompt = (await self._session.get_prompt(name,arguments))
        return prompt
    async def list_tool(self) -> list[types.Tool]:
        listtools = (await self._session.list_tools())
        return listtools.tools if listtools else []
    
    # async def call_tool(self,tool_name, *args, **kwargs):
    #     return await self._session.call_tool(tool_name, *args, **kwargs)
    
    async def list_resource(self) -> list[types.Resource]:
        result = await self._session.list_resources()
        return result.resources if result else []
    
    # async def read_resourse(self, uri:str)->types.ReadResourceResult:
    #     assert self._session,"Session unavailable, please reset"
    #     _url = AnyUrl(uri)
    #     # print(f" url = {_url}")
    #     result = await self._session.read_resource(_url)
    #     resource = result.contents[0]
    #     if isinstance(resource,types.TextResourceContents):
    #         if resource.mimeType == "application/json":
    #             try:
    #                 return json.loads(resource.text)
                    
    #             except json.decoder.JSONDecodeError as e:
    #                 print(f"JSON ERROR: {e}")
                    
    #     return resource.text
        
    #     # print(f"Dictionary of RESULT: {result.__dict__}")
    #     return result
        
    # async def read_resource_template(self) -> list[types.ResourceTemplate]:
    #     assert self._session,"Session Not Avaliable"
    #     result: types.ListResourceTemplatesResult = await self._session.list_resource_templates()
    #     # print("List Resource Template", result.__dict__)
    #     return result.resourceTemplates
async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        prompts = await client.list_prompts()
        print(prompts)
        prompt = await client.read_prompts()
        print("Prompts:", prompt)
        
        tools = await client.list_tool()
        print(f"Tools : {tools}")
        # for tool in tools:
        #     print(f"Availabe tool = {tool.name}")
        # if tools:
        #     for tool in tools:
        #         if tool.name =="read_doc":
        #             result = await client.call_tool(tool.name,)
        #             print(f"Result from {tool}:", result)
        resource = await client.list_resource()
        print("Resources:", resource)   
        
        # read_resource = await client.read_resourse(resource[0].uri)
        # # read_resource = await client.read_resourse('docs://documents')
        # print("data",read_resource)
        # print(type(read_resource))
        # resourselist = await client.list_resource()
        # print("Resource List = ", resourselist)
        # values = await client.read_resource_template()
        # url = values[0].uriTemplate
        # # for doc in client.list_resource():
        # all_resource = await client.read_resourse("docs://documents")
        # # print("all Resources : ", all_resource)
        
        # for r in all_resource:
        #     result = await client.read_resourse(url.replace("{doc_name}",r))
        #     print(result)
        
if __name__ == "__main__":
    asyncio.run(main())