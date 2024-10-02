from loguru import logger
from fastapi import HTTPException, status

from dto.warrior_dto import WarriorDto
from loaders.warrior import WarriorLoader
from loaders.exceptions import *

GenericWarriorDto = WarriorDto.Create | WarriorDto.Update | WarriorDto.UpdatePart

async def access_warrior(**kwargs):
    match kwargs['method']:
        case "get":
            try:
                return await WarriorLoader.get(kwargs['id'])
            except Exception as e:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        case "post":
            if isinstance(kwargs['dto'], WarriorDto.Create): 
                logger.info(f"Warrior DTO {kwargs['dto']} передан в access, POST")
                try:
                    return await WarriorLoader.create(army_id=kwargs['army_id'], dto=kwargs['dto'])
                except BaseLoaderException:
                    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            else:
                logger.error(f"Invalid DTO {kwargs['dto']}")
                raise ValueError("Invalid DTO")
        case "put", "patch":
            if isinstance(kwargs['dto'], WarriorDto.Update):
                logger.info(f"Warrior DTO {kwargs['dto']} передан в access, PUT")
                try: 
                    return await WarriorLoader.update(**kwargs)
                except BaseLoaderException:
                    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            else:
                logger.error(f"Invalid DTO {kwargs['dto']}")
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        case "delete":
            try:
                await WarriorLoader.delete(kwargs['id'])
            except Exception:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)