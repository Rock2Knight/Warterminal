import random
from loguru import logger
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator, confloat, conint

class Point(BaseModel):
    x: int
    y: int

    def move(self, x: int, y: int):
        self.x += x
        self.y += y
        return self


class BaseUnit:

    class BaseUnitCreate(BaseModel):
        health: confloat(ge=100.0) = 100.00
        damage: confloat(ge=10.0) = 10.0
        defense: confloat(ge=50.0) = 50
        coord: Point
        radius_dmg: conint(ge=1) = 10
        base_speed: int = 2
        dmg_coef: float = 1.5
        dto_name: str = ""    

    class BaseUnitUpdate(BaseModel):
        id: int
        health: Optional[confloat(ge=100.0)] = None
        damage: Optional[confloat(ge=10.0)] = None
        defense: Optional[confloat(ge=50.0)] = None
        coord: Optional[Point] = None
        radius_dmg: Optional[conint(ge=1)] = None
        base_speed: Optional[int] = None
        dmg_coef: Optional[float] = None

'''
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
'''