import asyncio
from typing import Optional
import random
from loguru import logger

from models import *
#from ..models import *

async def get_army_by_id(army_id: int):
    army = await Army.filter(id=army_id)
    logger.debug(f"Army {army_id}, content: {army}")
    if isinstance(army, list):
        if len(army) > 1:
            # Отладочная часть
            for arm in army:
                logger.debug(f"Army: {arm.id}, content: {arm.model_dump()}")
            # Отладочная часть (конец)
            army = army[-1]
        else:
            army = army[0]
    return army


    return army


async def get_army_units(army_id: int):
    """ Получить всех юнитов армии """
    wariors = await Warrior.filter(army_id=army_id).order_by('id')
    archers = await Archer.filter(army_id=army_id).order_by('id')
    varvars = await Varvar.filter(army_id=army_id).order_by('id')    
    
    units = wariors + archers + varvars
    if units:
        random.shuffle(units)
    return units


async def update_army_status(army_id: int, figths_with: int):
    """ Обновить противника армии """
    await Army.filter(id=army_id).update(fight_with_id=figths_with)
    updated_army = await Army.filter(id=army_id).first()
    return updated_army


async def is_exist_army(army_id: int):
    """ Проверить существует ли армия """
    exists = await Army.filter(id=army_id).exists()
    return bool(exists)


async def get_free_armies(army_id: int) -> Optional[list[Army]]:
    """ Получить все армии, которые сейчас не в бою """
    armies = await Army.all()
    if armies is None:
        return None
    new_armies = [army for army in armies]
    i = 0
    for army in new_armies:
        if army.fight_with_id == army_id:
            i = army
            break
    new_armies.pop(i) 
    return new_armies
