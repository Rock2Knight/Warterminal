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
        new_archer = Archer(army_id=archer.army_id, **update_dict)
        await new_archer.save()
        return new_archer
    except Exception as e:
        logger.error(f"Error while updating archer: {e}")
        raise UpdateModelException(f"Error while updating archer: {e}")


async def update_part_archer(update_dto: ArcherDto.UpdatePart) -> Archer:
    """ Реализация PATCH-запроса """
    archer = await get_archer(update_dto.id)
    archer_dict = await archer.values_dict(fk_fields=True)
    update_dict = update_dto.model_dump()
    
    attrs = [attr for attr, value in archer_dict.items()]
    attrs_updated = list([])
    attrs_non_updated = list([])

    for attr, value in update_dict.items():
        if hasattr(archer, attr) and value is not None:
            archer = await _update_archer(archer, attr, value)
        else:
            logger.error(f"Invalid attribute: {attr}")
            raise UpdateModelException(f"Invalid attribute: {attr}")
    
    archer = await get_archer(update_dto.id)
    return archer

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