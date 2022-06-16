import typing

import snowfin


__all__: typing.Sequence[str] = ("UtilitiesModule",)


class UtilitiesModule(snowfin.Module):
    @snowfin.slash_command("info", dm_permission=False)
    async def info_command(
        self, _: snowfin.Interaction
    ) -> tuple[snowfin.Embed, snowfin.Button]:
        """Shows the user information about Monks."""
        return (
            snowfin.Embed(
                "Information",
                "Monks is an endurance hosting bot developed with the use of snowfin and hikari.",
            ),
            snowfin.Button(
                "Source Code",
                style=snowfin.ButtonStyle.LINK,
                url="https://github.com/Shinobou/Monks",
            ),
        )
