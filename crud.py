import asyncio
from typing import Optional
import random
from loguru import logger

from models import *


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


async def get_army_units(army_id: int):
    wariors = await Warrior.filter(army_id=army_id).order_by('id')
    archers = await Archer.filter(army_id=army_id).order_by('id')
    varvars = await Varvar.filter(army_id=army_id).order_by('id')    
    
    units = wariors + archers + varvars
    if units:
        random.shuffle(units)
    return units


async def update_army_status(army_id: int, figths_with: int):
    await Army.filter(id=army_id).update(fight_with_id=figths_with)
    updated_army = await Army.filter(id=army_id).first()
    return updated_army


async def is_exist_army(army_id: int):
    exists = await Army.filter(id=army_id).exists()
    return bool(exists)


async def get_free_armies(army_id: int) -> Optional[list[Army]]:
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

async def get_concrete_unit(unit: AbstractUnit) -> AbstractUnit:
    if isinstance(unit, Warrior):
        res_unit = await Warrior.filter(id=unit.id).first()
        return res_unit
    elif isinstance(unit, Archer):
        res_unit = await Archer.filter(id=unit.id).first()
        return res_unit
    elif isinstance(unit, Varvar):
        res_unit = await Varvar.filter(id=unit.id).first()
        return res_unit
    else:
        raise ValueError(f"Unknown unit type: {type(unit)}")

async def delete_unit(unit: AbstractUnit):
    if isinstance(unit, Warrior):
        await Warrior.filter(id=unit.id).delete()
    elif isinstance(unit, Archer):
        await Archer.filter(id=unit.id).delete()
    elif isinstance(unit, Varvar):
        await Varvar.filter(id=unit.id).delete()
    else:
        raise ValueError(f"Unknown unit type: {type(unit)}")
