import snowfin
import hikari


class Client(snowfin.Client):
    def __init__(self, public_key: str, application_id: int, token: str) -> None:
        super().__init__(public_key, application_id, True, token, True)
        self.rest: hikari.impl.RESTClientImpl = hikari.RESTApp().acquire(
            token, hikari.TokenType.BOT
        )
