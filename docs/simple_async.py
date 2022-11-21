import asyncio
import random

import modal.aio

stub = modal.aio.AioStub("pubsub")


@stub.function
async def square(n: float) -> float:
    """square

    :param n: a float
    :return: the square of n
    """
    return n**2


async def main() -> None:
    """main

    An async entrypoint method is needed because Python doesn't allow async code
    in module scope.

    :return: None
    """
    async with stub.run():
        n = 100
        # executes n calls to square in parallel
        await asyncio.gather(*[square(random.random()) for i in range(n)])


if __name__ == "__main__":
    asyncio.run(main())
