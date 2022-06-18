from __future__ import annotations

import typing

from tortoise import models, fields


__all__: typing.Sequence[str] = ("Guild", "User")


class Guild(models.Model):
    id: int = fields.IntField(pk=True)
    starting_balance: typing.Optional[int] = fields.IntField(null=True, default=None)
    stonewood_cost: typing.Optional[int] = fields.IntField(null=True, default=None)
    plankerton_cost: typing.Optional[int] = fields.IntField(null=True, default=None)
    canny_valley_cost: typing.Optional[int] = fields.IntField(null=True, default=None)
    twine_peaks_cost: typing.Optional[int] = fields.IntField(null=True, default=None)
    hosting_channel_id: typing.Optional[int] = fields.IntField(null=True, default=None)


class User(models.Model):
    id: int = fields.IntField(pk=True)
    guild_id: int = fields.IntField()
    coins: int = fields.IntField()
    banned: fields.BooleanField = fields.BooleanField(default=False)
