from loaders.model_loader import ModelLoader
from loaders.exceptions import *
from crud.warrior import *


class WarriorLoader(ModelLoader):

    @classmethod
    async def get(cls, id: int):
        warrior = None
        try:
            logger.debug("In warrior loader")
            warrior = await get_warrior(id)
        except Exception as e:
            raise BaseLoaderException
        else:
            logger.debug("Мы получили warrior из базы")
            return await warrior.values_dict(fk_fields=True)

    @classmethod
    async def create(cls, **kwargs):
        warrior = await create_warrior(army_id=kwargs['army_id'], warrior_create_dto=kwargs['dto'])
        return await warrior.values_dict(fk_fields=True)
       
    @classmethod
    async def update(cls, **kwargs) -> Optional[Warrior]:
        match kwargs['method']:
            case 'put':
                try:
                    warrior = await update_full_warrior(kwargs['dto'])
                    if warrior is None:
                        return None
                    return warrior
                except Exception as e:
                    logger.error(f"Within updating warrior: {e}")
                    raise e                
            case 'patch':
                try:
                    warrior = await update_part_warrior(kwargs['dto'])
                    return warrior
                except Exception as e:
                    logger.error(f"Within updating warrior: {e}")
                    raise e

    @classmethod
    async def delete(cls, id: int):
        try:
            await delete_warrior(id)
        except BaseLoaderException as e:
            raise e