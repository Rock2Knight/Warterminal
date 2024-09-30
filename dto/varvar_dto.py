from base_schema import BaseUnit

class VarvarDto:

    class Create(BaseUnit.BaseUnitCreate):
        radius_dmg: int = 8
        base_speed: int = 2
        dmg_coef: float = 2.5
        dto_name: str = "Varvar"

    class Update(BaseUnit.BaseUnitUpdate):
        radius_dmg: int = 8
        base_speed: int = 2
        dmg_coef: float = 2.5
        dto_name: str = "Varvar"