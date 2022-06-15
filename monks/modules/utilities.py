import snowfin


class UtilitiesModule(snowfin.Module):
    """This is an example module"""

    @snowfin.slash_command("info")
    async def info_command(self, _: snowfin.Interaction):
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
