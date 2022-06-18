import tortoise
import typing


class Cache(list[tortoise.Model]):
    def __init__(self, model: typing.Type[tortoise.Model]) -> None:
        super().__init__()
        self._model: typing.Type[tortoise.Model] = model

    def start(self) -> None:
        [self.append(m) for m in model.all()]  # type: ignore

    async def update(self, model: tortoise.Model, **kwargs) -> None:
        for x in range(len(self)):
            if all(item in self[x].__dict__.items() for item in kwargs.items()):
                self[x] = model

    def get(self, **kwargs) -> typing.Union[tortoise.Model, None]:
        for model in self:
            if all(item in model.__dict__.items() for item in kwargs.items()):
                return model
