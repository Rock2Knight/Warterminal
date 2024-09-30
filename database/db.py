from configparser import ConfigParser
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


async def init():
    # Настройки БД
    '''
    await Tortoise.init(
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "database": config['db_name'],
                        "host": config['host'],
                        "password": config['password'],
                        "port": config['port'],
                        "user": config['user']
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
    '''
    await Tortoise.init(config = DB_CONFIG)
    # Генерация схемы
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(init())