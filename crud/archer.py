from typing import Optional, Any

from loguru import logger

from dto.base_schema import BaseUnit
from dto.archer_dto import ArcherDto
from models import Archer
from .exceptions import *


async def get_archer(archer_id: int) -> Optional[Archer]:
    return await Archer.get_or_none(id=archer_id)

async def create_archer(army_id: int, archer_create_dto: ArcherDto.Create) -> Archer:

    ##################################
    all_archers = await Archer.all().order_by('id')
    if all_archers:
        for archer in all_archers:
            logger.debug(f"{await archer.values_dict(fk_fields=True)}")
    else:
        logger.debug("No archers found")

    ##################################

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
            await Archer.filter(id=archer.id).update(health=value)
        case "damage": 
            await Archer.filter(id=archer.id).update(damage=value)
        case "defense":
            await Archer.filter(id=archer.id).update(defense=value)
        case "x_coord":
            await Archer.filter(id=archer.id).update(x_coord=value)
        case "y_coord":
            await Archer.filter(id=archer.id).update(y_coord=value)
        case "radius_dmg":
            await Archer.filter(id=archer.id).update(radius_dmg=value)
        case "base_speed":
            await Archer.filter(id=archer.id).update(base_speed=value)
        case "dmg_coef":
            await Archer.filter(id=archer.id).update(dmg_coef=value)



async def update_full_archer(update_dto: ArcherDto.Update) -> Archer:
    """ Реализация PUT-запроса """
    archer = await get_archer(update_dto.id)
    update_dict = update_dto.model_dump()

    try:
        for attr, value in update_dict.items():
            if attr == 'coord':
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