from imports import *

logger.add("debug_10_06.log", format="{time} | {level}   | {module}:{function}:{line} - {message}", level="DEBUG", backtrace=True)

app = FastAPI()

def init_router():
    for router in routers:
        app.include_router(router)

@app.on_event("startup")
async def startup_event():
    # Подключение и инициализация схем при старте
    register_tortoise(
        app,
        config=DB_CONFIG,
        generate_schemas=False,  # Автоматическое создание схем при старте
        add_exception_handlers=True,  # Добавляем обработчики ошибок для Tortoise
    )
    init_router()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("In shutdown")
    # Закрытие соединений при завершении работы приложения
    await Tortoise.close_connections()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True)