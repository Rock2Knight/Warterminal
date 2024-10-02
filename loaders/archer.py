from loaders.model_loader import ModelLoader
from loaders.exceptions import *
from crud.archer import *


class ArcherLoader(ModelLoader):

    @classmethod
    async def get(cls, id: int):
        archer = None
        try:
            archer = await get_archer(id)
        except Exception as e:
            raise BaseLoaderException
        else:
            return await archer.values_dict(fk_fields=True)

    @classmethod
    async def create(cls, **kwargs):
        archer = await create_archer(army_id=kwargs['army_id'], archer_create_dto=kwargs['dto'])
        return await archer.values_dict(fk_fields=True)
       
    @classmethod
    async def update(cls, **kwargs) -> Archer:
        if isinstance(kwargs['dto'], ArcherDto.Update):
            match kwargs['method']:
                case 'put':
                    try:
                        archer = await update_full_archer(kwargs['dto'])
                        return await archer
                    except Exception as e:
                        logger.error(f"Within updating archer: {e}")
                        raise e                
                case 'patch':
                    try:
                        archer = await update_part_archer(kwargs['dto'])
                        return await archer
                    except Exception as e:
                        logger.error(f"Within updating archer: {e}")
                        raise e
        else:
            raise BaseLoaderException

    @classmethod
    async def delete(cls, **kwargs):
        try:
            await delete_archer(id)
        except BaseLoaderException as e:
            raise e