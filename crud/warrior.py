from typing import Optional, Any

from loguru import logger

from dto.base_schema import BaseUnit
from dto.warrior_dto import WarriorDto
from models import *

from .exceptions import *


async def get_warrior(warrior_id: int) -> Optional[Warrior]:
    return await Warrior.get_or_none(id=warrior_id)

async def create_warrior(army_id: int, warrior_create_dto: WarriorDto.Create) -> Warrior:

    try:
        warrior = Warrior(
            army_id=army_id,
            health=warrior_create_dto.health,
            damage=warrior_create_dto.damage,
            defense=warrior_create_dto.defense,
            x_coord=warrior_create_dto.coord.x,
            y_coord=warrior_create_dto.coord.y,
            radius_dmg=warrior_create_dto.radius_dmg,
            base_speed=warrior_create_dto.base_speed,
            dmg_coef=warrior_create_dto.dmg_coef
        )
        await warrior.save()
        return warrior
    except Exception as e:
        logger.error(f"Error while creating warrior: {e}")
        raise CreateModelException(f"Error while creating warrior: {e}")


async def _update_warrior(warrior: Warrior, attr: str, value: Any) -> Warrior:
    match attr:
        case "health": 
            await Warrior.filter(id=warrior.id).update(health=value)
        case "damage": 
            await Warrior.filter(id=warrior.id).update(damage=value)
        case "defense":
            await Warrior.filter(id=warrior.id).update(defense=value)
        case "x_coord":
            await Warrior.filter(id=warrior.id).update(x_coord=value)
        case "y_coord":
            await Warrior.filter(id=warrior.id).update(y_coord=value)
        case "radius_dmg":
            await Warrior.filter(id=warrior.id).update(radius_dmg=value)
        case "base_speed":
            await Warrior.filter(id=warrior.id).update(base_speed=value)
        case "dmg_coef":
            await Warrior.filter(id=warrior.id).update(dmg_coef=value)



async def update_full_warrior(update_dto: WarriorDto.Update) -> Warrior:
    """ Реализация PUT-запроса """
    warrior = await get_warrior(update_dto.id)
    update_dict = update_dto.model_dump()

    try:
        new_warrior = Warrior(army_id=warrior.army_id, **update_dict)
        await new_warrior.save()
        return new_warrior
    except Exception as e:
        raise UpdateModelException


async def update_part_warrior(update_dto: WarriorDto.UpdatePart) -> Warrior:
    """ Реализация PATCH-запроса """
    warrior = await get_warrior(update_dto.id)
    warrior_dict = await warrior.values_dict(fk_fields=True)
    update_dict = update_dto.model_dump()
    
    attrs = [attr for attr, value in warrior_dict.items()]
    attrs_updated = list([])
    attrs_non_updated = list([])

    for attr, value in update_dict.items():
        if hasattr(warrior, attr) and value is not None:
            warrior = await _update_warrior(warrior, attr, value)
        else:
            logger.error(f"Invalid attribute: {attr}")
            raise UpdateModelException(f"Invalid attribute: {attr}")
    
    warrior = await get_warrior(update_dto.id)
    return warrior

async def delete_warrior(warrior_id: int):
    """ Реализация DELETE-запроса """
    warrior = await get_warrior(warrior_id)
    if warrior is None:
        return
    
    try:
        await Warrior.filter(id=warrior_id).delete()
    except Exception as e:
        logger.error(f"Error while deleting warrior: {e}")
        raise DeleteModelException(f"Error while deleting warrior: {e}")