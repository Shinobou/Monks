import typing

import snowfin


__all__: typing.Sequence[str] = ("EconomyModule",)

from monks.database import models


async def _create_user(
    context: snowfin.Interaction, user: snowfin.User, balance_offset: int = 0
) -> models.User | None:
    if guild := await models.Guild.get_or_none(id=context.guild_id):
        if guild.starting_balance:
            return await models.User.create(
                id=user.id,
                guild_id=context.guild_id,
                coins=guild.starting_balance + balance_offset,
            )
    return None


class EconomyModule(snowfin.Module):
    @snowfin.slash_command("coins", dm_permission=False)
    @snowfin.slash_option("user", "the user", snowfin.OptionType.USER)
    async def coins_command(
        self,
        context: snowfin.Interaction,
        user: snowfin.User | snowfin.Member | None = None,
    ) -> snowfin.Embed:
        """Shows how many coins a user has."""
        if not user:
            if user_from_member := context.author.user:
                user = user_from_member
            else:
                return snowfin.Embed("Error", f"Could not determine user.")

        if user_stats := await models.User.get_or_none(
            id=user.id, guild_id=context.guild_id
        ):
            return snowfin.Embed(
                "Coins", f"<@{user.id}> has **{user_stats.coins}** coin(s)."
            )

        if created_user := await _create_user(context, user):
            return snowfin.Embed(
                "Coins", f"<@{user.id}> has **{created_user.coins}** coin(s)."
            )

        return snowfin.Embed(
            "Error",
            f"This guild has not configured a starting balance yet. Please use `/config`.",
        )

    @snowfin.slash_command(
        "add_coins",
        default_member_permissions=snowfin.Permissions.ADMINISTRATOR,
        dm_permission=False,
    )
    @snowfin.slash_option("user", "the user", snowfin.OptionType.USER, required=True)
    @snowfin.slash_option(
        "amount", "the amount of coins", snowfin.OptionType.INTEGER, required=True
    )
    async def add_coins_command(
        self,
        context: snowfin.Interaction,
        user: snowfin.User | snowfin.Member,
        amount: int,
    ) -> snowfin.Embed:
        """Allows admins to add coins."""
        if isinstance(user, snowfin.Member):
            if user_from_member := user.user:
                user = user_from_member
            else:
                return snowfin.Embed("Error", f"Could not determine user.")

        if user_stats := await models.User.get_or_none(
            id=user.id, guild_id=context.guild_id
        ):
            await user_stats.update_from_dict({"coins": user_stats.coins + amount})
            await user_stats.save(update_fields=["coins"])
        else:
            await _create_user(context, user, amount)
        return snowfin.Embed("Added", f"Added **{amount}** coins to <@{user.id}>.")

    @snowfin.slash_command(
        "remove_coins",
        default_member_permissions=snowfin.Permissions.ADMINISTRATOR,
        dm_permission=False,
    )
    @snowfin.slash_option("user", "the user", snowfin.OptionType.USER, required=True)
    @snowfin.slash_option(
        "amount", "the amount of coins", snowfin.OptionType.INTEGER, required=True
    )
    async def remove_coins_command(
        self,
        context: snowfin.Interaction,
        user: snowfin.User | snowfin.Member,
        amount: int,
    ) -> snowfin.Embed:
        """Allows admins to remove coins."""
        if isinstance(user, snowfin.Member):
            if user_from_member := user.user:
                user = user_from_member
            else:
                return snowfin.Embed("Error", f"Could not determine user.")

        if user_stats := await models.User.get_or_none(
            id=user.id, guild_id=context.guild_id
        ):
            await user_stats.update_from_dict({"coins": user_stats.coins - amount})
            await user_stats.save(update_fields=["coins"])
        else:
            await _create_user(context, user, amount)
        return snowfin.Embed("Removed", f"Removed **{amount}** coins to <@{user.id}>.")
