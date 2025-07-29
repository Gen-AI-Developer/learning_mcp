from mcp.server.fastmcp import FastMCP

app = FastMCP(
    name="learning-mcp",
    stateless_http=True
    
)

server_app = app.streamable_http_app()