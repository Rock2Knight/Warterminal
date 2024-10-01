import pytest
#import asyncio

from tortoise import Tortoise

from models import *
from crud import warrior


async def init_db():
    # Настройки БД
    await Tortoise.init(
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "database": "ilshat_db",
                        "host": "localhost",
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


async def test_get_warrior():

    await init_db()

    test_warrior = {'dmg_coef': 1.5, 'id': 3, 'army_id': 2, 
            'x_coord': 2.0, 'defense': 50.0, 'health': 100.0, 
            'radius_dmg': 10, 'base_speed': 2, 'damage': 10.0, 
            'y_coord': 5.0, 'army': {'name': 'Orda', 'is_fail': False, 'id': 2, 'fight_with_id': 7, 'count': 8}}

    real_warrior = await warrior.get_warrior(3)
    assert real_warrior is not None
    real_warrior_dict = await real_warrior.values_dict(fk_fields=True) 
    assert real_warrior_dict == test_warrior


async def test_update_full_warrior():

    await init_db()

    test_warrior = Warrior(
        id=3,
        health=150,
        damage=10,
        defense=50,
        x_coord=2,
        y_coord=5,
        radius_dmg=10,
        base_speed=2,
        dmg_coef=1.5,
        army_id=2
    )

    updated_warrior = await warrior.update_full_warrior(3, health=150)

    assert updated_warrior is not None

    test_warrior_dict = await updated_warrior.values_dict(fk_fields=True)
    updated_warrior_dict = await updated_warrior.values_dict(fk_fields=True)

    assert test_warrior_dict == updated_warrior_dict


async def test_update_partially_warrior():

    await init_db()

    test_warrior = Warrior(
        id=3,
        health=200,
        damage=10,
        defense=50,
        x_coord=2,
        y_coord=5,
        radius_dmg=10,
        base_speed=2,
        dmg_coef=1.5,
        army_id=2
    )

    updated_warrior = await warrior.update_partially_warrior(3, health=200)

    assert updated_warrior is not None

    test_warrior_dict = await updated_warrior.values_dict(fk_fields=True)
    updated_warrior_dict = await updated_warrior.values_dict(fk_fields=True)

    assert test_warrior_dict == updated_warrior_dict