from fastapi import APIRouter, Response, status, HTTPException
from access.game import access_game
from dto.game_dto import Game
from views.fight import Fight

game_router = APIRouter(prefix="/game", tags=["Игра"])

@game_router.post("/{army_count}/{units_count}")
async def start_game(army_count: int, units_count: int, game: Game, response: Response):

    game_result = await Fight.init_fight(game)  # Запускаем игру
    if not isinstance(game_result, HTTPException):
        response.status_code = status.HTTP_201_CREATED
        return game_result
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return game_result     # Если возникла ошибка