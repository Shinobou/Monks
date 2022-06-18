import snowfin
import hikari

from monks.database import cache, models


class Client(snowfin.Client):
    def __init__(self, public_key: str, application_id: int, token: str) -> None:
        super().__init__(public_key, application_id, True, token, True)
        self.rest: hikari.impl.RESTClientImpl = hikari.RESTApp().acquire(
            token, hikari.TokenType.BOT
        )
        self.guild_cache: cache.Cache = cache.Cache(models.Guild)
        self.user_cache: cache.Cache = cache.Cache(models.User)
