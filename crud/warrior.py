from typing import Optional, Any

from loguru import logger

from dto.base_schema import BaseUnit
from dto.warrior_dto import WarriorDto
from models import *

from .exceptions import *


async def get_warrior(warrior_id: int) -> Optional[Warrior]:
    #warrior = Warrior.get_or_none(id=warrior_id)
    #logger.debug(f"warrior = {warrior}")
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
            warrior.health = value
        case "damage": 
            warrior.damage = value
        case "defense":
            warrior.defense = value
        case "x_coord":
            warrior.x_coord = value
        case "y_coord":
            warrior.y_coord = value
        case "radius_dmg":
            warrior.radius_dmg = value
        case "base_speed":
            warrior.base_speed = value
        case "dmg_coef":
            warrior.dmg_coef = value
    await warrior.save()
    return warrior



async def update_full_warrior(update_dto: WarriorDto.Update) -> Optional[Warrior]:
    """ Реализация PUT-запроса """
    warrior = await get_warrior(update_dto.id)
    if warrior is None:
        return None
    logger.debug(f"warrior = {warrior}")
    update_dict = update_dto.model_dump()

    try:
        for attr, value in update_dict.items():
            logger.debug(f"key = {attr}, value = {value}")
            if attr == 'coord':
                if value is None:
                    warrior = await _update_warrior(warrior, "x_coord", None)
                    logger.debug(f"warrior = {warrior}")
                    warrior = await _update_warrior(warrior, "y_coord", None)
                    logger.debug(f"warrior = {warrior}")
                else:
                    warrior = await _update_warrior(warrior, "x_coord", value.x)
                    logger.debug(f"warrior = {warrior}")
                    warrior = await _update_warrior(warrior, "y_coord", value.y)
                    logger.debug(f"warrior = {warrior}")
            else:
                warrior = await _update_warrior(warrior, attr, value)
                logger.debug(f"warrior = {warrior}")
        return warrior
    except Exception as e:
        logger.error(e.args)
        raise UpdateModelException


async def update_part_warrior(update_dto: WarriorDto.Update) -> Warrior:
    """ Реализация PATCH-запроса """
    warrior = await get_warrior(update_dto.id)
    update_dict = update_dto.model_dump()

    try:
        for attr, value in update_dict.items():
            if value is not None:
                if attr == 'coord':
                    warrior = await _update_warrior(warrior, "x_coord", value.x)
                    warrior = await _update_warrior(warrior, "y_coord", value.y)
                else:
                    warrior = await _update_warrior(warrior, attr, value)
        return warrior
    except Exception as e:
        raise UpdateModelException
    

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