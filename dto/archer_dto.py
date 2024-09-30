from base_schema import BaseUnit

class ArcherrDto:

    class Create(BaseUnit.BaseUnitCreate):
        radius_dmg: int = 20
        base_speed: int = 2
        dmg_coef: float = 1.5
        dto_name: str = "Archer"

    class Update(BaseUnit.BaseUnitUpdate):
        radius_dmg: int = 20
        base_speed: int = 2
        dmg_coef: float = 1.5
        dto_name: str = "Archer"