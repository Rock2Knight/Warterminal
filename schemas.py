import random
from abc import abstractmethod
from loguru import logger
from enum import Enum

from pydantic import BaseModel, validator, confloat, conint

logger.add("debug.log", format="{time} {level} {message}", level="INFO")

class Point(BaseModel):
    x: int
    y: int

    def move(self, x: int, y: int):
        self.x += x
        self.y += y
        return self


class BaseUnit(BaseModel):
    id: int
    health: confloat(ge=100.0) = 100.00
    damage: confloat(ge=10.0) = 10.0
    defense: confloat(ge=50.0) = 50
    coord: Point
    radius_dmg: conint(ge=1) = 10
    base_speed: int = 2
    dmg_coef: float = 1.5
    dto_name: str = ""


    @validator('coord')
    def validate_coord(cls, v, **kwargs):
        if not isinstance(v, Point):
            return ValueError('Неправильный тип поля')
        else:
            return v


class WarriorDto(BaseUnit):
    radius_dmg: int = 10
    base_speed: int = 2
    dmg_coef: float = 1.5
    dto_name: str = "Warrior"


class ArcherDto(BaseUnit):
    radius_dmg: int = 20
    base_speed: int = 2
    dmg_coef: float = 1.5
    dto_name: str = "Archer"


class VarvarDto(BaseUnit):
    radius_dmg: int = 8
    base_speed: int = 2
    dmg_coef: float = 2.5
    dto_name: str = "Varvar"


class ArmyDto(BaseModel):
    id: int
    name: str
    count: int
    units: dict[int, BaseUnit] = dict()

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


class ArmyStatBase(BaseModel):
    # Статистика по армии
    id: int
    name: str
    loss: int


class Game(BaseModel):
    id: int
    gmap: Point          # карта
    army_count: int
    units_count: int
    armies: list[ArmyDto]
    is_play: bool = True
    is_over: bool = False
    win_army: ArmyStatBase


class AbstractAttackDto(BaseModel):
    moving: Point
    attack: confloat(ge=0)
    radius_dmg: conint(ge=1)
    base_speed: conint(ge=1)
    dmg_coef: confloat(ge=1.0)