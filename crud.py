import asyncio
from typing import Optional

from tortoise.filters import Filter

from models imoprt *


async def get_army_by_id(army_id: int):
    army = await Army.filter(id__eq=army1_id)
    return army


async def get_army_units(army_id: int):
    wariors = await Warrior.all.filter(army_id__eq=army_id).order_by('id')
    archers = await Archer.all.filter(army_id__eq=army_id).order_by('id')
    varvars = await Varvar.all.filter(army_id__eq=army_id).order_by('id')    
    
    units = {'warrior': list(wariors), 'archer': list(archers), 'varvar': list(varvars)}

    return units


async def update_army_status(army_id: int, figths_with: int):
    await Army.filter(id__eq=army_id).update(fight_with_id=figths_with)
    updated_army = await Army.filter(id__eq=army_id).first()
    return updated_army


async def is_exist_army(army_id: int):
    exists = await Army.filter(id__eq=army_id).exists()
    return bool(exists)


async def get_free_armies(army_id: int) -> Optional[list[Army]]:
    armies = await Army.filter(id__neq=army_id)
    armies = armies.filter(fight_with_id__is_null=True)
    return armies if armies else None