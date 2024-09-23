from tortoise import Tortoise, run_async

async def init():
    # Настройки БД
    await Tortoise.init(
        db_url="postgres://postgres:asakura2150@127.0.0.1:5432/postgres",
        modules={"models": ["models"]}
    )
    # Генерация схемы
    await Tortoise.generate_schemas()