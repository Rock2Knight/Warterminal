from typing import Optional

from pydantic import BaseModel, confloat, conint

from .base_schema import Point, BaseUnit
from .army_dto import ArmyDto

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
    armies_id: list[int]
    is_play: bool = True
    is_over: bool = False
    win_army: Optional[ArmyStatBase] = None
    
class AbstractAttackDto(BaseModel):
    moving: Point
    attack: confloat(ge=0)
    radius_dmg: conint(ge=1)
    base_speed: conint(ge=1)
    dmg_coef: confloat(ge=1.0)