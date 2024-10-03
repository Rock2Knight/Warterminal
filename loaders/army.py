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

        if kwargs['army_dto_create'].units:
            for unit in kwargs['army_dto_create'].units.values():
                logger.debug(f"Unit is instance of {type(unit)}")
                unit_dump = {'dto': None, 'method': 'post'}
                match unit.dto_name:
                    case 'Warrior': 
                        warrior_dump = {'method': 'post', 'army_id': army.id,
                                'dto': WarriorDto.Create(**unit.model_dump())}
                        warrior_dump['method'] = 'post'
                        await access_warrior(**warrior_dump)
                    case 'Archer': 
                        archer_dump = {'method': 'post', 'army_id': army.id,
                                'dto': ArcherDto.Create(**unit.model_dump())}
                        archer_dump['method'] = 'post'
                        await access_archer(**archer_dump)
                    case 'Varvar': 
                        varvar_dump = {'method': 'post', 'army_id': army.id,
                                'dto': VarvarDto.Create(**unit.model_dump())}
                        varvar_dump['method'] = 'post'
                        await access_varvar(**varvar_dump)

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
                            army = await update_army_name(kwargs['army_id'], '')
                        else:
                            army = await update_army_name(kwargs['army_id'], kwargs['army_dto'].name)
                        if kwargs['army_dto'].count is None:
                            army = await update_army_units_count(kwargs['army_id'], '')
                        else:
                            army = await update_army_units_count(kwargs['army_id'], kwargs['army_dto'].count)
                        await Army.filter(id=kwargs['army_id']).update(fight_with_id=None)
                        army = await Army.filter(id=kwargs['army_id']).update(is_fail=False)
                    
                        if kwargs['army_dto'].units is not None:
                            
                            updated_units = list([])
                            # Обновляем методом PUT тех юнитов, которые были переданы в запросе
                            for unit in kwargs['army_dto'].units.values():
                                logger.debug(f"Unit is instance of {type(unit)}")
                                unit_dump = {'dto': unit, 'method': 'put'}
                                unit_dump['army_id'] = kwargs['army_dto'].id
                                if isinstance(unit, WarriorDto.Update):
                                    updated_units.append(await access_warrior(**unit_dump))
                                elif isinstance(unit, ArcherDto.Update):
                                    updated_units.append(await access_archer(**unit_dump))
                                elif isinstance(unit, VarvarDto.Update):
                                    updated_units.append(await access_varvar(**unit_dump))

                            all_units = await Army.filter(id=kwargs['army_dto'].id).all()
                            non_units = list(set(all_units)-set(updated_units))

                            # Удаляем тех юнитов, которые не были переданы в запросе
                            for unit in non_units:
                                if isinstance(unit, Warrior):
                                    await Warrior.filter(id=unit.id).delete()
                                elif isinstance(unit, Archer):
                                    await Warrior.filter(id=unit.id).delete()
                                elif isinstance(unit, Varvar):
                                    await Warrior.filter(id=unit.id).delete()

                        army = await get_army_by_id(kwargs['army_id'])
                        return await army.values_dict()
                    except Exception as e:
                        logger.error(f"Within updating army: {e}")
                        raise e                
                case 'patch':
                    try:
                        if kwargs['army_dto'].name is not None:
                            army = await update_army_name(kwargs['army_id'], kwargs['army_dto'].name)
                        if kwargs['army_dto'].count is not None:
                            army = await update_army_units_count(kwargs['army_id'], kwargs['army_dto'].count)
                        
                        if kwargs['army_dto'].units is not None:
                            updated_units = list([])
                            # Обновляем методом PATCH тех юнитов, которые были переданы в запросе
                            for unit in kwargs['army_dto'].units.values():
                                unit_dump = {'dto': unit, 'method': 'patch'}
                                unit_dump['army_id'] = kwargs['army_dto'].id
                                if unit.dto_name == "warrior":
                                    updated_units.append(await access_warrior(**unit_dump))
                                elif unit.dto_name == "archer":
                                    updated_units.append(await access_archer(**unit_dump))
                                elif unit.dto_name == "varvar":
                                    updated_units.append(await access_varvar(**unit_dump))

                        army_obj = await get_army_by_id(kwargs['army_id'])
                        return await army_obj.values_dict()
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