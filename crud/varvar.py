from typing import Optional, Any

from loguru import logger

from dto.base_schema import BaseUnit
from dto.varvar_dto import VarvarDto
from models import Varvar
from .exceptions import *


async def get_varvar(varvar_id: int) -> Optional[Varvar]:
    return await Varvar.get_or_none(id=varvar_id)

async def create_varvar(army_id: int, varvar_create_dto: VarvarDto.Create) -> Varvar:

    ##################################
    all_varvars = await Varvar.all().order_by('id')
    if all_varvars:
        for varvar in all_varvars:
            logger.debug(f"{await varvar.values_dict(fk_fields=True)}")
    else:
        logger.debug("No varvars found")

    ##################################

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
            await Varvar.filter(id=varvar.id).update(health=value)
        case "damage": 
            await Varvar.filter(id=varvar.id).update(damage=value)
        case "defense":
            await Varvar.filter(id=varvar.id).update(defense=value)
        case "x_coord":
            await Varvar.filter(id=varvar.id).update(x_coord=value)
        case "y_coord":
            await Varvar.filter(id=varvar.id).update(y_coord=value)
        case "radius_dmg":
            await Varvar.filter(id=varvar.id).update(radius_dmg=value)
        case "base_speed":
            await Varvar.filter(id=varvar.id).update(base_speed=value)
        case "dmg_coef":
            await Varvar.filter(id=varvar.id).update(dmg_coef=value)



async def update_full_varvar(update_dto: VarvarDto.Update) -> Varvar:
    """ Реализация PUT-запроса """
    varvar = await get_varvar(update_dto.id)
    update_dict = update_dto.model_dump()

    try:
        for attr, value in update_dict.items():
            if attr == 'coord':
                varvar = await _update_varvar(varvar, "x_coord", value.x)
                varvar = await _update_varvar(varvar, "y_coord", value.y)
            else:
                varvar = await _update_varvar(varvar, attr, value)
        return varvar
    except Exception as e:
        raise UpdateModelException



async def update_part_varvar(update_dto: VarvarDto.UpdatePart) -> Varvar:
    """ Реализация PATCH-запроса """
    varvar = await get_varvar(update_dto.id)
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