from loguru import logger

from dto.warrior_dto import WarriorDto
from loaders.warrior import WarriorLoader

GenericWarriorDto = WarriorDto.Create | WarriorDto.Update | WarriorDto.UpdatePart

async def access_warrior(**kwargs):
    match kwargs['method']:
        case "get":
            pass
        case "post":
            logger.debug(f"Warrior DTO: {kwargs['dto']}, type = {type(kwargs['dto'])}")
            if isinstance(kwargs['dto'], WarriorDto.Create): 
                logger.info(f"Warrior DTO {kwargs['dto']} передан в access, POST")
                return await WarriorLoader.create(army_id=kwargs['army_id'], dto=kwargs['dto'])
            else:
                logger.error(f"Invalid DTO {kwargs['dto']}")
                raise ValueError("Invalid DTO")
        case "put":
            pass
        case "delete":
            pass
        case "patch":
            pass