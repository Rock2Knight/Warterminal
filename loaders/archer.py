from loaders.model_loader import ModelLoader
from crud.archer import *


class ArcherLoader(ModelLoader):

    @classmethod
    async def create(cls, **kwargs):
        await create_archer(army_id=kwargs['army_id'], archer_create_dto=kwargs['dto'])
       
    @classmethod
    async def update(cls, **kwargs):
        pass

    @classmethod
    async def delete(cls, **kwargs):
        pass