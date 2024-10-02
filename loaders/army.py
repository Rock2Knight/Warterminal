import asyncio

from loguru import logger

from access.warrior import access_warrior
from access.archer import access_archer
from access.varvar import access_varvar

from loaders.model_loader import ModelLoader
from loaders.warrior import WarriorLoader
from loaders.archer import ArcherLoader
from loaders.varvar import VarvarLoader
from loaders.exceptions import *

from crud.army import *

from dto.army_dto import ArmyDto
from dto.warrior_dto import WarriorDto
from dto.archer_dto import ArcherDto
from dto.varvar_dto import VarvarDto

from models import Army

class ArmyLoader(ModelLoader):

    @classmethod
    async def create(cls, **kwargs):
        army = None

        try:
            army = await create_army(kwargs['army_dto_create'].name, kwargs['army_dto_create'].count)
        except Exception as e:
            logger.error(f"Within creating army: {e}")
            raise e

        for unit in kwargs['army_dto_create'].units.values():
            logger.debug(f"Unit is instance of {type(unit)}")
            unit_dump = {'dto': None, 'method': 'post'}
            if isinstance(unit, WarriorDto.Create):
                logger.debug("Unit is instance of warrior")
                unit_dump['dto'] = unit
                unit_dump['army_id'] = kwargs['army_dto_create'].id
                await access_warrior(**unit_dump)
            elif isinstance(unit, ArcherDto.Create):
                logger.debug("Unit is instance of archer")
                unit_dump['dto'] = unit
                unit_dump['army_id'] = kwargs['army_dto_create'].id
                await access_archer(**unit_dump)
            elif isinstance(unit, VarvarDto.Create):
                logger.debug("Unit is instance of varvar")
                unit_dump['dto'] = unit
                unit_dump['army_id'] = kwargs['army_dto_create'].id
                await access_varvar(**unit_dump)

        return await army.values_dict()


    @classmethod
    async def get(cls, id: int):
        try:
            army = await get_army_by_id(id)
        except Exception as e:
            raise BaseLoaderException
        else:
            return await army.values_dict()

        
    @classmethod
    async def update(cls, **kwargs):
        if isinstance(kwargs['army_dto'], ArmyDto.Update):
            match kwargs['method']:
                case 'put':
                    try:
                        if kwargs['army_dto'].name is None:
                            army = await update_army_name(kwargs['id'], '')
                        else:
                            army = await update_army_name(kwargs['id'], kwargs['army_dto'].name)
                        if kwargs['army_dto'].count is None:
                            army = await update_army_units_count(kwargs['id'], '')
                        else:
                            army = await update_army_units_count(kwargs['id'], kwargs['army_dto'].count)
                        await Army.filter(id=kwargs['id']).update(fight_with_id=None)
                        army = await Army.filter(id=kwargs['id']).update(is_fail=False)
                    
                        if kwargs['army_dto'].units is not None:
                            
                            updated_units = list([])
                            # Обновляем методом PUT тех юнитов, которые были переданы в запросе
                            for unit in kwargs['army_dto'].units.values():
                                logger.debug(f"Unit is instance of {type(unit)}")
                                unit_dump = {'dto': None, 'method': 'put'}
                                if isinstance(unit, WarriorDto.Update):
                                    logger.debug("Unit is instance of warrior")
                                    unit_dump['dto'] = unit
                                    unit_dump['army_id'] = kwargs['army_dto'].id
                                    updated_units.append(await access_warrior(**unit_dump))
                                elif isinstance(unit, ArcherDto.Update):
                                    logger.debug("Unit is instance of archer")
                                    unit_dump['dto'] = unit
                                    unit_dump['army_id'] = kwargs['army_dto'].id
                                    updated_units.append(await access_archer(**unit_dump))
                                elif isinstance(unit, VarvarDto.Update):
                                    logger.debug("Unit is instance of varvar")
                                    unit_dump['dto'] = unit
                                    unit_dump['army_id'] = kwargs['army_dto'].id
                                    updated_units.append(await access_varvar(**unit_dump))

                            all_units = await Army.filter(army_id=kwargs['army_dto'].id).all()
                            non_units = list(set(all_units)-set(updated_units))

                            # Удаляем тех юнитов, которые не были переданы в запросе
                            for unit in non_units:
                                if isinstance(unit, Warrior):
                                    await Warrior.filter(id=unit.id).delete()
                                elif isinstance(unit, Archer):
                                    await Warrior.filter(id=unit.id).delete()
                                elif isinstance(unit, Varvar):
                                    await Warrior.filter(id=unit.id).delete()

                        return await army.values_dict()
                    except Exception as e:
                        logger.error(f"Within updating army: {e}")
                        raise e                
                case 'patch':
                    try:
                        if kwargs['army_dto'].name is not None:
                            army = await update_army_name(kwargs['id'], kwargs['army_dto'].name)
                        if kwargs['army_dto'].count is not None:
                            army = await update_army_units_count(kwargs['id'], kwargs['army_dto'].count)
                        
                        if kwargs['army_dto'].units is not None:
                            updated_units = list([])
                            # Обновляем методом PATCH тех юнитов, которые были переданы в запросе
                            for unit in kwargs['army_dto'].units.values():
                                logger.debug(f"Unit is instance of {type(unit)}")
                                unit_dump = {'dto': None, 'method': 'patch'}
                                if isinstance(unit, WarriorDto.Update):
                                    logger.debug("Unit is instance of warrior")
                                    unit_dump['dto'] = unit
                                    unit_dump['army_id'] = kwargs['army_dto'].id
                                    updated_units.append(await access_warrior(**unit_dump))
                                elif isinstance(unit, ArcherDto.Update):
                                    logger.debug("Unit is instance of archer")
                                    unit_dump['dto'] = unit
                                    unit_dump['army_id'] = kwargs['army_dto'].id
                                    updated_units.append(await access_archer(**unit_dump))
                                elif isinstance(unit, VarvarDto.Update):
                                    logger.debug("Unit is instance of varvar")
                                    unit_dump['dto'] = unit
                                    unit_dump['army_id'] = kwargs['army_dto'].id
                                    updated_units.append(await access_varvar(**unit_dump))

                        return await army.values_dict()
                    except Exception as e:
                        logger.error(f"Within updating army: {e}")
                        raise e
        else:
            raise BaseLoaderException


    @classmethod
    async def delete(cls, id: int):
        try:
            await delete_army(id)
        except BaseLoaderException as e:
            raise e