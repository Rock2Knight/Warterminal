from typing import Optional

from pydantic import BaseModel, conint, confloat

from .base_schema import BaseUnit, Point
    
class WarriorDto:

    class Create(BaseUnit.BaseUnitCreate):
        radius_dmg: int = 10
        base_speed: int = 2
        dmg_coef: float = 1.5
        dto_name: str = "Warrior"

    class Update(BaseModel):
        id: int
        health: Optional[confloat(ge=100.0)] = None
        damage: Optional[confloat(ge=10.0)] = None
        defense: Optional[confloat(ge=50.0)] = None
        coord: Optional[Point] = None
        radius_dmg: Optional[conint(ge=1)] = None
        base_speed: Optional[int] = None
        dmg_coef: Optional[float] = None
        dto_name: Optional[str] = None