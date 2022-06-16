import typing

import snowfin


__all__: typing.Sequence[str] = ("ConfigModule",)

from monks.database import models


class ConfigModule(snowfin.Module):
    @snowfin.slash_command(
        "config",
        default_member_permissions=snowfin.Permissions.ADMINISTRATOR,
        dm_permission=False,
    )
    async def config_command(self, _: snowfin.Interaction) -> snowfin.ModalResponse:
        """Opens up a menu to edit the config."""
        return snowfin.ModalResponse(
            "config_modal",
            "Config",
            [
                snowfin.TextInput("starting_balance", label="Starting Balance"),
                snowfin.TextInput("stonewood_cost", label="Stonewood Cost"),
                snowfin.TextInput("plankerton_cost", label="Plankerton Cost"),
                snowfin.TextInput("canny_valley_cost", label="Canny Valley Cost"),
                snowfin.TextInput("twine_peaks_cost", label="Twine Peaks Cost"),
            ],
        )

    @snowfin.modal_callback("config_modal")
    async def config_modal_callback(
        self, context: snowfin.Interaction
    ) -> snowfin.Embed:
        data: snowfin.ModalSubmit = context.data  # type: ignore
        values: list[int] = []

        for component in data.components:
            if value := component.components[0].value:
                try:
                    values.append(int(value))
                except ValueError:
                    return snowfin.Embed("Error", "You must enter a valid integer.")
            else:
                return snowfin.Embed("Error", "You can't leave any field blank.")

        await models.Guild.update_or_create(
            {
                "starting_balance": int(values[0]),
                "stonewood_cost": int(values[1]),
                "plankerton_cost": int(values[2]),
                "canny_valley_cost": int(values[3]),
                "twine_peaks_cost": int(values[4]),
            },
            id=int(context.guild_id),
        )

        return snowfin.Embed(
            "Updated", "This guild's config has been updated successfully."
        )

    @snowfin.slash_command(
        "set_channel",
        default_member_permissions=snowfin.Permissions.ADMINISTRATOR,
        dm_permission=False,
    )
    @snowfin.slash_option(
        "channel",
        "The hosting channel you want to use.",
        snowfin.OptionType.CHANNEL,
        required=True,
    )
    async def set_channel_command(
        self, context: snowfin.Interaction, channel: snowfin.Channel
    ) -> snowfin.Embed:
        await models.Guild.update_or_create(
            {"hosting_channel_id": channel.id}, id=int(context.guild_id)
        )
        return snowfin.Embed("Updated", f"Set hosting channel to <#{channel.id}>.")
