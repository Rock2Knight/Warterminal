from loaders.model_loader import ModelLoader
from crud.varvar import *

class VarvarLoader(ModelLoader):

    @classmethod
    async def create(cls, **kwargs):
        await create_varvar(army_id=kwargs['army_id'], varvar_create_dto=kwargs['dto'])
       
    @classmethod
    async def update(cls, **kwargs):
        pass

    @classmethod
    async def delete(cls, **kwargs):
        pass