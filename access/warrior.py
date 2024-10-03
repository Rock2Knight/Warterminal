from typing import Optional

from loguru import logger
from fastapi import HTTPException, status

from dto.warrior_dto import WarriorDto
from loaders.warrior import WarriorLoader
from loaders.exceptions import *

from models import Warrior

async def access_warrior(**kwargs) -> Optional[Warrior | HTTPException]:
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
        case "put":
            try: 
                res = await WarriorLoader.update(**kwargs)
                return res
            except BaseLoaderException:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        case 'patch':
            try: 
                return await WarriorLoader.update(**kwargs)
            except BaseLoaderException:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        case "delete":
            try:
                await WarriorLoader.delete(kwargs['id'])
            except Exception:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)