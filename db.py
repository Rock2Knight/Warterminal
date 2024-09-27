from tortoise import Tortoise, run_async



async def init():
    # Настройки БД
    await Tortoise.init(
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "database": "ilshat_db",
                        "host": "127.0.0.1",
                        "password": "asakura2150",
                        "port": 5432,
                        "user": "ilshat_user"
                    }
                }
            },
            "apps": {
                "models": {
                    "models": ["models"],
                    "default_connection": "default",
                }
            },
        }
    )
    # Генерация схемы
    await Tortoise.generate_schemas()