from loguru import logger

from dto.game_dto import Game
from dto.army_dto import ArmyDto

from loaders.army import ArmyLoader
from loaders.game import GameLoader

async def access_army(**kwargs):
    army_dump = dict()
    army_dump['method'] = kwargs['method']  # Для определения различий между PUT и PATCH

    match kwargs['method']:
        case "get":
            pass
        case "post":
            if isinstance(kwargs['army_dto'], ArmyDto.Create):
                #logger.debug(f"Army dto: {kwargs['army_dto']}")
                army_dump['army_dto_create'] = kwargs['army_dto']
                await ArmyLoader.create(**army_dump)
        case "put", "patch":
            pass
        case "delete":
            pass