from loguru import logger

from dto.game_dto import Game
from loaders.game import GameLoader
from access.army import access_army

async def access_game(method: str, game: Game):
    game_dump = dict()
    game_dump['method'] = method  # Для определения различий между PUT и PATCH

    match method:
        case "get":
            pass
        case "post":
            for army in game.armies:                  # army - экземпляр типа ArmyDto.Create
                game_dump['army_dto'] = army
                logger.debug(f"Информация об игре: \{game_dump}\n\n")
                await access_army(**game_dump)
        case "put", "patch":
            pass
        case "delete":
            pass