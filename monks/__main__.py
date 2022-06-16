import asyncio
import os
import pathlib

import snowfin
import tortoise


async def on_start() -> None:
    await tortoise.Tortoise.init(
        db_url="sqlite://database.sqlite3",
        modules={"models": ["monks.database.models"]},
    )
    await tortoise.Tortoise.generate_schemas()


async def on_stop() -> None:
    await tortoise.Tortoise.close_connections()


def main() -> None:
    client: snowfin.Client = snowfin.Client(
        verify_key=os.environ["PUBLIC_KEY"],
        application_id=int(os.environ["APPLICATION_ID"]),
        sync_commands=True,
        token=os.environ["DISCORD_TOKEN"],
        auto_defer=True,
    )

    for path in pathlib.Path("./monks/modules").glob("*.py"):
        client.load_module(str(path).replace("\\", ".").replace(".py", ""))

    try:
        asyncio.get_running_loop().run_until_complete(on_start())
    except RuntimeError:
        asyncio.new_event_loop().run_until_complete(on_start())

    client.run("0.0.0.0", 5000)

    try:
        asyncio.get_running_loop().run_until_complete(on_stop())
    except RuntimeError:
        asyncio.new_event_loop().run_until_complete(on_stop())


if __name__ == "__main__":
    main()
