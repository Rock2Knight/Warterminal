from models import *

async def get_concrete_unit(unit: AbstractUnit) -> AbstractUnit:
    if isinstance(unit, Warrior):
        res_unit = await Warrior.filter(id=unit.id).first()
        return res_unit
    elif isinstance(unit, Archer):
        res_unit = await Archer.filter(id=unit.id).first()
        return res_unit
    elif isinstance(unit, Varvar):
        res_unit = await Varvar.filter(id=unit.id).first()
        return res_unit
    else:
        raise ValueError(f"Unknown unit type: {type(unit)}")

async def delete_unit(unit: AbstractUnit):
    if isinstance(unit, Warrior):
        await Warrior.filter(id=unit.id).delete()
    elif isinstance(unit, Archer):
        await Archer.filter(id=unit.id).delete()
    elif isinstance(unit, Varvar):
        await Varvar.filter(id=unit.id).delete()
    else:
        raise ValueError(f"Unknown unit type: {type(unit)}")