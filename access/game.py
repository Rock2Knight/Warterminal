from ..schemas import Game

async def access_game(method: str, game: Game):
    match method:
        case "get":
            pass
        case "post":
            pass
        case "put":
            pass
        case "delete":
            pass
        case "patch":
            pass