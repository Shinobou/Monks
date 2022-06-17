import typing

import snowfin


__all__: typing.Sequence[str] = ("ConfigModule",)

from monks.database import models


class ConfigModule(snowfin.Module):
    set_command: snowfin.SlashCommand = snowfin.SlashCommand(
        name="set",
        default_member_permissions=snowfin.Permissions.ADMINISTRATOR,
        dm_permission=False,
    )

    view_command: snowfin.SlashCommand = snowfin.SlashCommand(
        name="view",
        default_member_permissions=snowfin.Permissions.ADMINISTRATOR,
        dm_permission=False,
    )

    @set_command.subcommand("prices", "sets the prices")
    async def set_prices_command(self, _: snowfin.Interaction) -> snowfin.ModalResponse:
        """Opens up a menu to set the prices of the config."""
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

    @set_command.subcommand("channel")
    @snowfin.slash_option(
        "channel",
        "The hosting channel you want to use.",
        snowfin.OptionType.CHANNEL,
        required=True,
    )
    async def set_channel_command(
        self, context: snowfin.Interaction, channel: snowfin.Channel
    ) -> snowfin.Embed:
        """Sets the hosting channel."""
        if not channel.type == snowfin.ChannelType.GUILD_TEXT:
            return snowfin.Embed("Error", "This must be a guild text channel.")

        await models.Guild.update_or_create(
            {"hosting_channel_id": channel.id}, id=context.guild_id
        )
        return snowfin.Embed("Updated", f"Set hosting channel to <#{channel.id}>.")

    @view_command.subcommand("config")
    async def view_config_command(self, context: snowfin.Interaction) -> snowfin.Embed:
        if guild := await models.Guild.get_or_none(id=context.guild_id):
            return (
                snowfin.Embed("Config")
                .add_field("Starting Balance", str(guild.starting_balance))
                .add_field("Stonewood Cost", str(guild.stonewood_cost))
                .add_field("Plankerton Cost", str(guild.plankerton_cost))
                .add_field("Canny Valley Cost", str(guild.canny_valley_cost))
                .add_field("Twine Peaks Cost", str(guild.twine_peaks_cost))
                .add_field("Hosting Channel", f"<#{guild.hosting_channel_id}>")
            )
