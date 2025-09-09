import os
import logging

import dotenv
import asyncio
from aiohttp import web

dotenv.load_dotenv()
from bot import bot_main  # noqa: E402


async def index(request):
    return web.Response(text="Hello, World!")


async def health(request):
    return web.Response(text="I am alive!")


def main():
    async def create_web_app():
        asyncio.create_task(bot_main())
        app = web.Application()
        app.router.add_get("/", index)
        app.router.add_get("/health", health)
        return app

    web.run_app(create_web_app(), host="0.0.0.0", port=os.environ.get("POST", 8008))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
