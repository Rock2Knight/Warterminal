from loaders.model_loader import ModelLoader
from crud.warrior import *


class WarriorLoader(ModelLoader):

    @classmethod
    async def create(cls, **kwargs):
        await create_warrior(army_id=kwargs['army_id'], warrior_create_dto=kwargs['dto'])
       
    @classmethod
    async def update(cls, **kwargs):
        pass

    @classmethod
    async def delete(cls, **kwargs):
        pass