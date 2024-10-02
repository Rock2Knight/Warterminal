import asyncio

from loguru import logger

from access.warrior import access_warrior
from access.archer import access_archer
from access.varvar import access_varvar

from loaders.model_loader import ModelLoader
from loaders.warrior import WarriorLoader
from loaders.archer import ArcherLoader
from loaders.varvar import VarvarLoader

from crud.army import *

from dto.warrior_dto import WarriorDto
from dto.archer_dto import ArcherDto
from dto.varvar_dto import VarvarDto

class ArmyLoader(ModelLoader):

    @classmethod
    async def create(cls, **kwargs):
        tasks = None
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


    @classmethod
    async def get(cls, **kwargs):
        pass
        
    @classmethod
    async def update(cls, **kwargs):
        match kwargs['method']:
            case 'put':
                pass
            case 'patch':
                pass

    @classmethod
    async def delete(cls, **kwargs):
        pass