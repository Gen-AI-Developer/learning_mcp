import asyncio
from contextlib import asynccontextmanager

# @asynccontextmanager
# async def make_connection(name):
#     print(f"Connecting to ......{name}")
#     yield name
#     print(f"Connected to {name}")

# async def main():
#     async with make_connection("mcp_server") as con:
#         print(f"Using Connection...{con}")

# asyncio.run(main())

#  @asynccontextmanager write this code for you.
async def get_connection(name):
    class Ctx():
        async def __aenter__(self):
            print(f"ENTER:->{name}")
            return name
        async def __aexit__(self, exc_type,exc,tb):
            print(f"EXIT:->{name}")
            # return name
    return Ctx()

async def main():
    async with await get_connection("server_a") as server_a:
        async with await get_connection("server_b") as server_b:
            print(f"USING CONNECTION:-> {server_a} and {server_b}")
asyncio.run(main())