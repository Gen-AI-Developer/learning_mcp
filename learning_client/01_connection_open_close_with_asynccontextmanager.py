import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def make_connection(name):
    print(f"Connecting to ......{name}")
    yield name
    print(f"Connected to {name}")

async def main():
    async with make_connection("mcp_server") as con:
        print(f"Using Connection...{con}")

asyncio.run(main())
