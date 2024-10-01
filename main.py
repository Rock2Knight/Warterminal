from imports import *

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", backtrace=True)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Подключение и инициализация схем при старте
    register_tortoise(
        app,
        config=DB_CONFIG,
        generate_schemas=True,  # Автоматическое создание схем при старте
        add_exception_handlers=True,  # Добавляем обработчики ошибок для Tortoise
    )

@app.on_event("shutdown")
async def shutdown_event():
    # Закрытие соединений при завершении работы приложения
    await Tortoise.close_connections()


@app.post("/game/{army_count}/{units_count}")
async def start_game(army_count: int, units_count: int, game: Game):

    game_result = await Fight.init_fight(game)  # Запускаем игру
    return game_result.model_dump()