from imports import *

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", backtrace=True)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Подключение и инициализация схем при старте
    register_tortoise(
        app,
        config=DB_CONFIG,
        generate_schemas=False,  # Автоматическое создание схем при старте
        add_exception_handlers=True,  # Добавляем обработчики ошибок для Tortoise
    )

@app.on_event("shutdown")
async def shutdown_event():
    # Закрытие соединений при завершении работы приложения
    await Tortoise.close_connections()


@app.post("/game/{army_count}/{units_count}")
async def start_game(army_count: int, units_count: int, game: Game, response: Response):

    game_result = await Fight.init_fight(game)  # Запускаем игру
    if isinstance(game_result, Game):
        response.status_code = status.HTTP_201_CREATED
        return game_result.model_dump()
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return game_result     # Если возникла ошибка