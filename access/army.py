from loguru import logger

from dto.game_dto import Game
from dto.army_dto import ArmyDto

from loaders.army import ArmyLoader
from loaders.game import GameLoader

GenericArmyDto = ArmyDto.Create | ArmyDto.Update | list[ArmyDto.Create] | list[ArmyDto.Update]

async def access_army(**kwargs):
    army_dump = dict()
    army_dump['method'] = kwargs['method']  # Для определения различий между PUT и PATCH

    match kwargs['method']:
        case "get":
            pass
        case "post":
            logger.info(f"Army dto: {kwargs['army_dto']}")
            if isinstance(kwargs['army_dto'], list[ArmyDto.Create]):
                for army in kwargs['army_dto']:                  # army - экземпляр типа ArmyDto.Create
                    army_dump['army_dto_create'] = army
                    logger.debug(f"Army dump: \n {army_dump}\n\n")
                    await ArmyLoader.create(**army_dump)
        case "put", "patch":
            pass
        case "delete":
            pass