import snowfin
import tortoise


class LifetimeModule(snowfin.Module):
    @snowfin.listen("start")
    async def start(self) -> None:
        self.client.rest.start()
        await tortoise.Tortoise.init(
            db_url="sqlite://database.sqlite3",
            modules={"models": ["monks.database.models"]},
        )
        await tortoise.Tortoise.generate_schemas()

    @snowfin.listen("stop")
    async def stop(self) -> None:
        await tortoise.Tortoise.close_connections()
