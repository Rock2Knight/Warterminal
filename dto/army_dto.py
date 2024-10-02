import random
from loguru import logger
from typing import Optional

from pydantic import BaseModel, validator, confloat, conint

from .base_schema import Point, BaseUnit
from .warrior_dto import WarriorDto
from .archer_dto import ArcherDto
from .varvar_dto import VarvarDto

class ArmyDto:

    class Create(BaseModel):
        id: int
        name: str
        count: int
        units: dict[int, WarriorDto.Create | VarvarDto.Create | ArcherDto.Create] = dict()

    class Update(BaseModel):
        id: int
        name: Optional[str]
        count: Optional[int]
        units: Optional[dict[int, WarriorDto.Update | VarvarDto.Update | ArcherDto.Update]]

    '''
    def add_unit(self, count: int, voins: list[BaseUnit]):
        print("\nVoins in add_unit func:  ", [str(v) for v in voins])
        print(f"Count of voins: {len(voins)}")

        while count > 0:
            try:
                ind = random.randint(0, len(voins) - 1)
            except ValueError as ve:
                print(f"Count of voins: {len(voins)}")
                logger.error(message="Count of voins less or equal 0")
                return
            self.units[voins[ind].id] = voins[ind]
            self.count += 1
            voins.pop(ind)
            count -= 1
    '''