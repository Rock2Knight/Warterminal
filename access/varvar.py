from typing import Optional

from loguru import logger
from fastapi import HTTPException, status

from dto.varvar_dto import VarvarDto
from loaders.varvar import VarvarLoader
from loaders.exceptions import *
from models import Varvar

async def access_varvar(**kwargs) -> Optional[Varvar | HTTPException]:
    match kwargs['method']:
        case "get":
            try:
                return await VarvarLoader.get(kwargs['id'])
            except Exception as e:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        case "post":
            if isinstance(kwargs['dto'], VarvarDto.Create): 
                logger.success(f"Varvar DTO {kwargs['dto']} передан в access, POST")
                return await VarvarLoader.create(army_id=kwargs['army_id'], dto=kwargs['dto'])
            else:
                logger.error(f"Invalid DTO {kwargs['dto']}")
                raise ValueError("Invalid DTO")
        case "put":
            logger.success(f"Varvar DTO {kwargs['dto']} передан в access, PUT")
            try: 
                res = await VarvarLoader.update(**kwargs)
                return res
            except BaseLoaderException:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        case "patch":
            logger.debug("In patch")
            logger.success(f"Varvar DTO {kwargs['dto']} передан в access, PATCH")
            try: 
                res = await VarvarLoader.update(**kwargs)
                return res
            except BaseLoaderException:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        case "delete":
            try:
                await VarvarLoader.delete(id=kwargs['id'])
            except Exception:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)