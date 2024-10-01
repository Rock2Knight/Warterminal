from loguru import logger

from dto.archer_dto import ArcherDto
from loaders.archer import ArcherLoader

GenericArcherDto = ArcherDto.Create | ArcherDto.Update | ArcherDto.UpdatePart

async def access_archer(**kwargs):
    match kwargs['method']:
        case "get":
            pass
        case "post":
            if isinstance(kwargs['dto'], ArcherDto.Create): 
                logger.info(f"Archer DTO {kwargs['dto']} передан в access, POST")
                return await ArcherLoader.create(army_id=kwargs['army_id'], dto=kwargs['dto'])
            else:
                logger.error(f"Invalid DTO {kwargs['dto']}")
                raise ValueError("Invalid DTO")
        case "put":
            pass
        case "delete":
            pass
        case "patch":
            pass