from loaders.model_loader import ModelLoader
from loaders.exceptions import *
from crud.varvar import *

class VarvarLoader(ModelLoader):

    @classmethod
    async def get(cls, id: int):
        archer = None
        try:
            archer = await get_varvar(id)
        except Exception as e:
            raise BaseLoaderException
        else:
            return await archer.values_dict(fk_fields=True)

    @classmethod
    async def create(cls, **kwargs):
        varvar = await create_varvar(army_id=kwargs['army_id'], varvar_create_dto=kwargs['dto'])
        return await varvar.values_dict(fk_fields=True)
       
    @classmethod
    async def update(cls, **kwargs) -> Varvar:
        if isinstance(kwargs['dto'], VarvarDto.Update):
            match kwargs['method']:
                case 'put':
                    try:
                        varvar = await update_full_varvar(kwargs['dto'])
                        return await varvar
                    except Exception as e:
                        logger.error(f"Within updating varvar: {e}")
                        raise e                
                case 'patch':
                    try:
                        varvar = await update_part_varvar(kwargs['dto'])
                        return await varvar
                    except Exception as e:
                        logger.error(f"Within updating varvar: {e}")
                        raise e
        else:
            raise BaseLoaderException

    @classmethod
    async def delete(cls, **kwargs):
        try:
            await delete_varvar(id)
        except BaseLoaderException as e:
            raise e