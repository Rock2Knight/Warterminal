from typing import Optional, Any

from loguru import logger

from dto.base_schema import BaseUnit
from dto.archer_dto import ArcherDto
from models import Archer
from .exceptions import *


async def get_archer(archer_id: int) -> Optional[Archer]:
    return await Archer.get_or_none(id=archer_id)

async def create_archer(army_id: int, archer_create_dto: ArcherDto.Create) -> Archer:
    try:
        archer = Archer(
            army_id=army_id,
            health=archer_create_dto.health,
            damage=archer_create_dto.damage,
            defense=archer_create_dto.defense,
            x_coord=archer_create_dto.coord.x,
            y_coord=archer_create_dto.coord.y,
            radius_dmg=archer_create_dto.radius_dmg,
            base_speed=archer_create_dto.base_speed,
            dmg_coef=archer_create_dto.dmg_coef
        )
        await archer.save()
        return archer
    except Exception as e:
        logger.error(f"Error while creating archer: {e}")
        raise CreateModelException(f"Error while creating archer: {e}")


async def _update_archer(archer: Archer, attr: str, value: Any) -> Archer:
    match attr:
        case "health": 
            archer.health = value
        case "damage": 
            archer.damage = value
        case "defense":
            archer.defense = value
        case "x_coord":
            archer.x_coord = value
        case "y_coord":
            archer.y_coord = value
        case "radius_dmg":
            archer.radius_dmg = value
        case "base_speed":
            archer.base_speed = value
        case "dmg_coef":
            archer.dmg_coef = value
    await archer.save()
    return archer



async def update_full_archer(update_dto: ArcherDto.Update) -> Optional[Archer]:
    """ Реализация PUT-запроса """
    archer = await get_archer(update_dto.id)
    if archer is None:
        return None
    update_dict = update_dto.model_dump()

    try:
        for attr, value in update_dict.items():
            if attr == 'coord':
                if value is None:
                    archer = await _update_archer(archer, "x_coord", None)
                    archer = await _update_archer(archer, "y_coord", None)
                else:
                    archer = await _update_archer(archer, "x_coord", value.x)
                    archer = await _update_archer(archer, "y_coord", value.y)
            else:
                archer = await _update_archer(archer, attr, value)
        return archer
    except Exception as e:
        raise UpdateModelException


async def update_part_archer(update_dto: ArcherDto.Update) -> Archer:
    """ Реализация PATCH-запроса """
    archer = await get_archer(update_dto.id)
    update_dict = update_dto.model_dump()

    try:
        for attr, value in update_dict.items():
            if value is not None:
                if attr == 'coord':
                    archer = await _update_archer(archer, "x_coord", value.x)
                    archer = await _update_archer(archer, "y_coord", value.y)
                else:
                    archer = await _update_archer(archer, attr, value)
        return archer
    except Exception as e:
        raise UpdateModelException

async def delete_archer(archer_id: int):
    """ Реализация DELETE-запроса """
    archer = await get_archer(archer_id)
    if archer is None:
        return
    
    try:
        await Archer.filter(id=archer_id).delete()
    except Exception as e:
        logger.error(f"Error while deleting archer: {e}")
        raise DeleteModelException(f"Error while deleting archer: {e}")