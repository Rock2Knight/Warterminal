from base_schema import BaseUnit
    
class WarriorDto:

    class Create(BaseUnit.BaseUnitCreate):
        radius_dmg: int = 10
        base_speed: int = 2
        dmg_coef: float = 1.5
        dto_name: str = "Warrior"

    class Update(BaseUnit.BaseUnitUpdate):
        radius_dmg: int = 10
        base_speed: int = 2
        dmg_coef: float = 1.5
        dto_name: str = "Warrior"