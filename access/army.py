from loguru import logger
from fastapi import HTTPException, status

from dto.game_dto import Game
from dto.army_dto import ArmyDto

from loaders.army import ArmyLoader
from loaders.game import GameLoader
from loaders.exceptions import *

async def access_army(**kwargs):
    army_dump = dict()
    army_dump['method'] = kwargs['method']  # Для определения различий между PUT и PATCH
    method_res = None

    match kwargs['method']:
        case "get":
            try:
                return await ArmyLoader.get(kwargs['id'])
            except Exception as e:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        case "post":
            if isinstance(kwargs['army_dto'], ArmyDto.Create):
                #logger.debug(f"Army dto: {kwargs['army_dto']}")
                army_dump['army_dto_create'] = kwargs['army_dto']
                try:
                    return await ArmyLoader.create(**army_dump)
                except BaseLoaderException:
                    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        case "put", "patch":
            if isinstance(kwargs['army_dto'], ArmyDto.Update):
                try:
                    return await ArmyLoader.update(**kwargs)
                except Exception as e:
                    if isinstance(e, BaseLoaderException):
                        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
                    else:
                        raise e
        case "delete":
            try:
                await ArmyLoader.delete(kwargs['id'])
            except Exception:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
