from loguru import logger

from dto.varvar_dto import VarvarDto
from loaders.varvar import VarvarLoader

GenericVarvarDto = VarvarDto.Create | VarvarDto.Update | VarvarDto.UpdatePart

async def access_varvar(**kwargs):
    match kwargs['method']:
        case "get":
            pass
        case "post":
            if isinstance(kwargs['dto'], VarvarDto.Create): 
                logger.info(f"Varvar DTO {kwargs['dto']} передан в access, POST")
                return await VarvarLoader.create(army_id=kwargs['army_id'], dto=kwargs['dto'])
            else:
                logger.error(f"Invalid DTO {kwargs['dto']}")
                raise ValueError("Invalid DTO")
        case "put":
            pass
        case "delete":
            pass
        case "patch":
            pass