from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="learning-mcp",
    stateless_http=True
    
)
docs = {
    "introduction": "This is a learning MCP server.",
    "description": "This server is designed to demonstrate the capabilities of the MCP framework.",
    "guidelines": "Follow the documentation for using the tools and resources provided by this server.",
}
@mcp.resource(uri="docs://documents",name="docs", description="Get documentation information",minetype="application/json")
async def get_docs():
    return list(docs.keys())

server_app = mcp.streamable_http_app()