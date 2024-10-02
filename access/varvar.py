from loguru import logger
from fastapi import HTTPException, status

from dto.varvar_dto import VarvarDto
from loaders.varvar import VarvarLoader
from loaders.exceptions import *

GenericVarvarDto = VarvarDto.Create | VarvarDto.Update | VarvarDto.UpdatePart

async def access_varvar(**kwargs):
    match kwargs['method']:
        case "get":
            try:
                return await VarvarLoader.get(kwargs['id'])
            except Exception as e:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        case "post":
            if isinstance(kwargs['dto'], VarvarDto.Create): 
                logger.info(f"Varvar DTO {kwargs['dto']} передан в access, POST")
                return await VarvarLoader.create(army_id=kwargs['army_id'], dto=kwargs['dto'])
            else:
                logger.error(f"Invalid DTO {kwargs['dto']}")
                raise ValueError("Invalid DTO")
        case "put", "patch":
            if isinstance(kwargs['dto'], VarvarDto.Update):
                logger.info(f"Varvar DTO {kwargs['dto']} передан в access, PUT")
                try: 
                    return await VarvarLoader.update(**kwargs)
                except BaseLoaderException:
                    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            else:
                logger.error(f"Invalid DTO {kwargs['dto']}")
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        case "delete":
            try:
                await VarvarLoader.delete(kwargs['id'])
            except Exception:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)