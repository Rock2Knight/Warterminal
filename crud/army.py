import asyncio
from typing import Optional
import random
from loguru import logger

from models import *
from .exceptions import *


async def create_army(name: str, count: int, is_failed: bool = False, 
            fight_with: Optional[int]=None) -> Army:
    army = await Army.create(name=name, count=count, is_failed=is_failed, fight_with_id=fight_with)
    return army


async def get_army_by_id(army_id: int) -> Army:
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


async def get_army_units(army_id: int) -> list[AbstractUnit]:
    """ Получить всех юнитов армии """
    wariors = await Warrior.filter(army_id=army_id).order_by('id')
    archers = await Archer.filter(army_id=army_id).order_by('id')
    varvars = await Varvar.filter(army_id=army_id).order_by('id')    
    
    units = wariors + archers + varvars
    if units:
        random.shuffle(units)
    return units


async def update_army_status(army_id: int, figths_with: int) -> Army:
    """ Обновить противника армии """
    try:
        await Army.filter(id=army_id).update(fight_with_id=figths_with)
        updated_army = await Army.filter(id=army_id).first()
        return updated_army
    except Exception as e:
        logger.error(f"Ошибка при обновлении армии {army_id}: {e}")
        raise UpdateModelException(f"Ошибка при обновлении армии {army_id}")
    
async def update_army_name(army_id: int, name: str) -> Army:
    """ Изменить название армии """
    try:
        await Army.filter(id=army_id).update(name=name)
        updated_army = await Army.filter(id=army_id).first()
        return updated_army
    except Exception as e:
        logger.error(f"Ошибка при обновлении имени армии {army_id}")
        raise UpdateModelException(f"Ошибка при обновлении имени армии {army_id}")
    
async def update_army_units_count(army_id: int, count: int) -> Army:
    """ Изменить начальное количество юнитов армии """
    try:
        await Army.filter(id=army_id).update(count=count)
        updated_army = await Army.filter(id=army_id).first()
        return updated_army
    except Exception as e:
        logger.error(f"Ошибка при обновлении количества юнитов армии {army_id}")
        raise UpdateModelException(f"Ошибка при обновлении количества юнитов армии {army_id}")



async def is_exist_army(army_id: int) -> bool:
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

async def delete_army(army_id: int):
    army = await get_army_by_id(army_id)
    if army is None:
        return
    
    try:
        await Army.filter(id=army_id).delete()
    except Exception as e:
        logger.error(f"Error while deleting army: {e}")
        raise DeleteModelException(f"Error while deleting army: {e}")