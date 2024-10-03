import json
import random

from dto.base_schema import BaseUnit, Point
from dto.warrior_dto import WarriorDto
from dto.archer_dto import ArcherDto
from dto.varvar_dto import VarvarDto

def generate_objects(num_objects: int, dto_name: str):
    objects = []
    for _ in range(num_objects):
        new_dict = {
            "health": random.randint(10, 120),
            "damage": random.randint(10, 15),
            "defense": random.randint(50, 70),
            "base_speed": 2,
            'dto_name': dto_name
        }
        match dto_name:
            case "warrior":
                new_dict['radius_dmg'] = random.randint(10, 15)
                new_dict['dmg_coef'] = float(random.randint(150, 200)) / 100
            case "archer":
                new_dict['radius_dmg'] = random.randint(20, 25)
                new_dict['dmg_coef'] = float(random.randint(150, 200)) / 100
            case "varvar":
                new_dict['radius_dmg'] = random.randint(8, 13)
                new_dict['dmg_coef'] = float(random.randint(250, 300)) / 100
        objects.append(new_dict)
    return objects

warriors = generate_objects(20, 'warrior')
archers = generate_objects(20, 'archer')
varvars = generate_objects(20, 'varvar')

with open("warriors.json", "w") as file:
    json.dump(warriors, file)
with open("archers.json", "w") as file:
    json.dump(archers, file)
with open("varvars.json", "w") as file:
    json.dump(varvars, file)