import json

from loguru import logger
from tortoise import Tortoise, run_async

config = None

with open("./database/config.json", 'r') as f:
    config = json.load(f)

# Настройка подключения к БД
DB_CONFIG = {
    "connections": {
        "default": f"postgres://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db_name']}"
    },
    "apps": {
        "models": {
            "models": ["models"],  # Указываем, где находятся модели
            "default_connection": "default",
        }
    }
}

'''
async def init():
    # Настройки БД
    await Tortoise.init(
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "database": db_config.db_name,
                        "host": db_config.host,
                        "password": db_config.password,
                        "port": db_config.port,
                        "user": db_config.user
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
'''