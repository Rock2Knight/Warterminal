from typing import Optional

from loguru import logger
from fastapi import HTTPException, status

from dto.archer_dto import ArcherDto
from loaders.archer import ArcherLoader
from loaders.exceptions import *

from models import Archer

async def access_archer(**kwargs) -> Optional[Archer | HTTPException]:
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
        case "put":
            if isinstance(kwargs['dto'], ArcherDto.Update):
                logger.info(f"Archer DTO {kwargs['dto']} передан в access, PUT")
                try: 
                    res = await ArcherLoader.update(**kwargs)
                    return res
                except BaseLoaderException:
                    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            else:
                logger.error(f"Invalid DTO {kwargs['dto']}")
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        case "patch":
            logger.info(f"Archer DTO {kwargs['dto']} передан в access, PATCH")
            try: 
                return await ArcherLoader.update(**kwargs)
            except BaseLoaderException:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        case "delete":
            try:
                await ArcherLoader.delete(id=kwargs['id'])
            except Exception as e:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)