import asyncio
from typing import Optional
import random

from loguru import logger

from schemas import BaseUnit, WarriorDto
from models import *


async def get_warrior(warrior_id: int) -> Optional[Warrior]:
    return await Warrior.get_or_none(id=warrior_id)

async def create_warrior(army_id: int, warrior_dto: WarriorDto) -> Warrior:

    try:
        warrior = Warrior(
            army_id=army_id,
            health=warrior_dto.health,
            damage=warrior_dto.damage,
            defense=warrior_dto.defense,
            x_coord=warrior_dto.coord.x,
            y_coord=warrior_dto.coord.y,
            radius_dmg=warrior_dto.radius_dmg,
            base_speed=warrior_dto.base_speed,
            dmg_coef=warrior_dto.dmg_coef
        )
        await warrior.save()
        return warrior
    except Exception as e:
        logger.error(f"Error while creating warrior: {e}")
        raise e


async def update_full_warrior(warrior_id: int, **kwargs) -> Warrior:
    """ Реализация PUT-запроса """
    warrior = await get_warrior(warrior_id)
    new_warrior = Warrior(army_id=warrior.army_id, **kwargs)
    await new_warrior.save()
    return new_warrior
    '''
    warrior_dict = await warrior.values_dict(fk_fields=True)
    print(f'\n{warrior_dict}\n')
    attrs = [attr for attr, value in warrior_dict.items()]
    attrs_updated = list([])
    attrs_non_updated = list([])

    for attr, value in kwargs.items():
        if hasattr(warrior, attr):
            attrs_updated.append(attr)
            setattr(warrior, attr, value)
        else:
            logger.error(f"Invalid attribute: {attr}")
            raise Exception(f"Invalid attribute: {attr}")
        
    attrs_non_updated = list(set(attrs) - set(attrs_updated))

    for attr in attrs_non_updated:
        if hasattr(warrior, attr):
            attrs_updated.append(attr)
            setattr(warrior, attr, None)
        else:
            logger.error(f"Invalid attribute: {attr}")
            raise Exception(f"Invalid attribute: {attr}")

    await warrior.save()
    return warrior
    '''
