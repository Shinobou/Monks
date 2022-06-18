import typing

import snowfin
import hikari


__all__: typing.Sequence[str] = ("HostingModule",)

from monks.database import models


class HostingModule(snowfin.Module):
    active_hosts: list[int] = []
    active_claims: list[int] = []
    ZONES: typing.Final[dict[str, str]] = {
        "Stonewood": "stone",
        "Plankerton": "plank",
        "Canny Valley": "canny",
        "Twine Peaks": "twine",
    }

    def _get_zone(self, zone: str) -> typing.Optional[str]:
        for key, value in self.ZONES.items():
            if value in zone.lower():
                return key
        return None

    @snowfin.slash_command("host", dm_permission=False)
    async def host_command(
        self, context: snowfin.Interaction
    ) -> typing.Union[snowfin.ModalResponse, snowfin.Embed]:
        """Shows the user information about Monks."""
        # TODO: add a spots option to the modal (spots are how many spots are avaliable in the endurance)
        print(context)
        if member := context.member:
            if user := member.user:
                if (
                    user.id not in self.active_hosts
                    and user.id not in self.active_claims
                ):
                    return snowfin.ModalResponse(
                        "host_modal",
                        "Details",
                        [
                            snowfin.TextInput("username", "Username"),
                            snowfin.TextInput("zone", "Zone"),
                            snowfin.TextInput(
                                "wave", "Wave", min_length=1, max_length=2
                            ),
                            snowfin.TextInput(
                                "notes", "Notes", snowfin.TextStyleTypes.PARAGRAPH
                            ),
                        ],
                    )
                return snowfin.Embed(
                    "Error",
                    "You can't host if you are in a claimed endurance or are already actively hosting.",
                )
        return snowfin.Embed("Error", "Could not find user.")

    @snowfin.modal_callback("host_modal")
    async def host_modal_callback(self, context: snowfin.Interaction):
        data: snowfin.ModalSubmit = context.data  # type: ignore

        values: dict[str, str] = {}

        for component in data.components:
            if c := component.components[0]:
                values[c.custom_id] = c.value
            else:
                return snowfin.Embed("Error", "You can't leave any field blank.")

        if zone := self._get_zone(values["zone"]):
            values["zone"] = zone
        else:
            return snowfin.Embed(
                "Error",
                "Invalid zone: must contain either stone, plank, canny, or twine.",
            )

        if not (values["wave"].isnumeric() and 1 <= int(values["wave"]) <= 30):
            return snowfin.Embed(
                "Error", "Invalid wave: must be an integer between 1 and 30."
            )

        if guild := await models.Guild.get_or_none(id=context.guild_id):
            if hosting_channel_id := guild.hosting_channel_id:
                message: hikari.Message = await self.client.rest.create_message(
                    hosting_channel_id,
                    hikari.Embed(title=f"{values['zone']} - Wave {values['wave']}")
                    .add_field("Username", values["username"])
                    .add_field("Notes", values["notes"]),
                )
                thread: hikari.GuildThreadChannel = await self.client.rest.create_message_thread(
                    hosting_channel_id,
                    message,
                    f"{values['zone']} - Wave {values['wave']} - {values['username']}",
                )

                await self.client.rest.add_thread_member(
                    thread.id, context.member.user.id
                )

                return snowfin.Embed(
                    "Hosting",
                    f"Hosting your endurance in <#{hosting_channel_id}>",
                    url=message.make_link(context.guild_id),
                )

        return snowfin.Embed(
            "Error", "This guild still needs to configure some settings in the config."
        )
