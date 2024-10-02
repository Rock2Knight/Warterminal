from loguru import logger
from fastapi import HTTPException, status

from dto.archer_dto import ArcherDto
from loaders.archer import ArcherLoader
from loaders.exceptions import *

GenericArcherDto = ArcherDto.Create | ArcherDto.Update | ArcherDto.UpdatePart

async def access_archer(**kwargs):
    match kwargs['method']:
        case "get":
            try:
                return await ArcherLoader.get(kwargs['id'])
            except Exception as e:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        case "post":
            if isinstance(kwargs['dto'], ArcherDto.Create): 
                logger.info(f"Archer DTO {kwargs['dto']} передан в access, POST")
                return await ArcherLoader.create(army_id=kwargs['army_id'], dto=kwargs['dto'])
            else:
                logger.error(f"Invalid DTO {kwargs['dto']}")
                raise ValueError("Invalid DTO")
        case "put", "patch":
            if isinstance(kwargs['dto'], ArcherDto.Update):
                logger.info(f"Archer DTO {kwargs['dto']} передан в access, PUT")
                try: 
                    return await ArcherLoader.update(**kwargs)
                except BaseLoaderException:
                    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            else:
                logger.error(f"Invalid DTO {kwargs['dto']}")
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        case "delete":
            try:
                await ArcherLoader.delete(kwargs['id'])
            except Exception:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)