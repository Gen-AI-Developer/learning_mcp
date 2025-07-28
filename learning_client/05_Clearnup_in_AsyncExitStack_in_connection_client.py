import asyncio
from contextlib import asynccontextmanager, AsyncExitStack

    # Async context manager for dynamic management of a stack of exit
    # callbacks.

    # For example:
    #     async with AsyncExitStack() as stack:
    #         connections = [await stack.enter_async_context(get_connection())
    #             for i in range(5)]
    #         # All opened connections will automatically be released at the
    #         # end of the async with statement, even if attempts to open a
    #         # connection later in the list raise an exception.
    

async def get_connection(name):
    class Ctx():
        async def __aenter__(self):
            print(f"ENTER:->{name}")
            return name
        async def __aexit__(self, exc_type,exc,tb):
            print(f"EXIT:->{name}")
            # return name
    return Ctx()

# async def main():
#     async with await get_connection("server_a") as server_a:
#         async with await get_connection("server_b") as server_b:
#             print(f"USING CONNECTION:-> {server_a} and {server_b}")
# asyncio.run(main())

async def main():
    async with AsyncExitStack() as stack:
        a = await stack.enter_async_context(await get_connection("server_a"))
        b = await stack.enter_async_context(await get_connection("server_b"))
        print(f"USING CONNECTION:-> {a} and {b}")

asyncio.run(main())