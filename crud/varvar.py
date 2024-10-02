from typing import Optional, Any

from loguru import logger

from dto.base_schema import BaseUnit
from dto.varvar_dto import VarvarDto
from models import Varvar
from .exceptions import *


async def get_varvar(varvar_id: int) -> Optional[Varvar]:
    return await Varvar.get_or_none(id=varvar_id)

async def create_varvar(army_id: int, varvar_create_dto: VarvarDto.Create) -> Varvar:

    try:
        varvar = Varvar(
            army_id=army_id,
            health=varvar_create_dto.health,
            damage=varvar_create_dto.damage,
            defense=varvar_create_dto.defense,
            x_coord=varvar_create_dto.coord.x,
            y_coord=varvar_create_dto.coord.y,
            radius_dmg=varvar_create_dto.radius_dmg,
            base_speed=varvar_create_dto.base_speed,
            dmg_coef=varvar_create_dto.dmg_coef
        )
        await varvar.save()
        return varvar
    except Exception as e:
        logger.error(f"Error while creating varvar: {e}")
        raise CreateModelException(f"Error while creating varvar: {e}")


async def _update_varvar(varvar: Varvar, attr: str, value: Any) -> Varvar:
    match attr:
        case "health": 
            varvar.health = value
        case "damage": 
            varvar.damage = value
        case "defense":
            varvar.defense = value
        case "x_coord":
            varvar.x_coord = value
        case "y_coord":
            varvar.y_coord = value
        case "radius_dmg":
            varvar.radius_dmg = value
        case "base_speed":
            varvar.base_speed = value
        case "dmg_coef":
            varvar.dmg_coef = value
    await varvar.save()
    return varvar



async def update_full_varvar(update_dto: VarvarDto.Update) -> Varvar:
    """ Реализация PUT-запроса """
    varvar = await get_varvar(update_dto.id)
    update_dict = update_dto.model_dump()

    try:
        for attr, value in update_dict.items():
            if attr == 'coord':
                if value is None:
                    varvar = await _update_varvar(varvar, "x_coord", None)
                    varvar = await _update_varvar(varvar, "y_coord", None)
                else:
                    varvar = await _update_varvar(varvar, "x_coord", value.x)
                    varvar = await _update_varvar(varvar, "y_coord", value.y)
            else:
                varvar = await _update_varvar(varvar, attr, value)
        return varvar
    except Exception as e:
        raise UpdateModelException



async def update_part_varvar(update_dto: VarvarDto.Update) -> Optional[Varvar]:
    """ Реализация PATCH-запроса """
    varvar = await get_varvar(update_dto.id)
    if varvar is None:
        return None
    update_dict = update_dto.model_dump()

    try:
        for attr, value in update_dict.items():
            if value is not None:
                if attr == 'coord':
                    varvar = await _update_varvar(varvar, "x_coord", value.x)
                    varvar = await _update_varvar(varvar, "y_coord", value.y)
                else:
                    varvar = await _update_varvar(varvar, attr, value)
        return varvar
    except Exception as e:
        raise UpdateModelException

async def delete_varvar(varvar_id: int):
    """ Реализация DELETE-запроса """
    varvar = await get_varvar(varvar_id)
    if varvar is None:
        return
    
    try:
        await Varvar.filter(id=varvar_id).delete()
    except DeleteModelException as e:
        logger.error(f"Error while deleting varvar: {e}")
        raise DeleteModelException(f"Error while deleting varvar: {e}")