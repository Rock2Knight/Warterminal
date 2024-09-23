import random
from abc import abstractmethod
from loguru import logger

from pydantic import BaseModel

logger.add("debug.log", format="{time} {level} {message}", level="INFO")

class Point(BaseModel):
    x: int
    y: int

    def __add__(self, other):
        return Point(x=self.x+other.x, y=self.y+other.y)

    def __sub__(self, other):
        return Point(x=self.x-other.x, y=self.y-other.y)

    def move(self, x: int, y: int):
        self.x += x
        self.y += y
        return self


class BaseUnit(BaseModel):
    id: int
    health: float = 100.00
    damage: float = 10.0
    defense: float = 50
    coord: Point
    radius_dmg: int
    base_speed: int
    dmg_coef: float

    def damaged(self, damage: float) -> int:
        if self.health > 0:
            if self.defense > 25:
                self.health -= 0.5 * damage
                self.defense -= 10
            elif self.defense > 0:
                self.health -= 0.8 * damage
                self.defense -= 5
            else:
                self.health -= damage
        if self.health <= 0:
            return self.id
        return -1

    def __str__(self):
        return str(self.id)


    async def attack(self, map1: Point, unit):
        dist = unit.coord - self.coord
        in_radius = abs(dist.x) < self.radius_dmg and abs(dist.y) < self.radius_dmg
        if not in_radius:
            self.move_to(unit, map1, 2)
            dist = unit.coord - self.coord
        if abs(dist.x) < self.radius_dmg and abs(dist.y) < self.radius_dmg:
            p = random.choice(list(range(5)))
            match p:
                case 0 | 1: return None
                case 2 | 3: return unit.damaged(self.damage)
                case 4:
                    damage = self.damage * self.dmg_coef
                    return unit.damaged(damage)


    def move_to(self, unit, map1: Point, speed: int = 1):
        p_move = random.random()
        x_move, y_move = False, False
        if abs(unit.coord.x - self.coord.x) > abs(unit.coord.y - self.coord.y):
            x_move = True
        else:
            y_move = True

        p_move = random.random()
        if x_move:
            if unit.coord.x < self.coord.x:
                self.coord.x = self.coord.x - 2 * speed
            else:
                self.coord.x = self.coord.x + 2 * speed
        else:
            if unit.coord.y < self.coord.y:
                self.coord.y = self.coord.y - 2 * speed
            else:
                self.coord.y = self.coord.y + 2 * speed

        if self.coord.x < 0:
            self.coord.x = 1
        elif self.coord.x > map1.x:
            self.coord.x = map1.x - 1
        if self.coord.y < 0:
            self.coord.y = 1
        elif self.coord.y > map1.y:
            self.coord.y = map1.y - 1


class Warrior(BaseUnit):
    radius_dmg: float = 10
    base_speed: int = 2
    dmg_coef: float = 1.5

    '''
        def attack(self, map1: Point, unit: BaseUnit) -> int | None:
        dist = unit.coord - self.coord
        in_radius = abs(dist.x) < self.radius_dmg and abs(dist.y) < self.radius_dmg
        if not in_radius:
            self.move_to(unit, map1, 2)
            dist = unit.coord - self.coord
        if abs(dist.x) < self.radius_dmg and abs(dist.y) < self.radius_dmg:
            p = random.random()
            if p > self.p_crit:
                damage = self.damage * 1.5
                return unit.damaged(damage)
            elif p > 0.5:
                return unit.damaged(self.damage)
            else:
                return None
    '''


class Archer(BaseUnit):
    radius_dmg: float = 20
    base_speed: int = 2
    dmg_coef: float = 1.5

    '''
        def attack(self, map1: Point, unit: BaseUnit) -> int | None:
        dist = Point(x=unit.coord.x-self.coord.x, y=unit.coord.y-self.coord.y)
        in_radius = abs(dist.x) < self.radius_dmg and abs(dist.y) < self.radius_dmg
        if not in_radius:
            self.move_to(unit, map1)
            dist = Point(x=unit.coord.x - self.coord.x, y=unit.coord.y - self.coord.y)
        if abs(dist.x) < self.radius_dmg and abs(dist.y) < self.radius_dmg:
            p = random.random()
            if p > self.p_crit:
                damage = self.damage * 1.5
                return unit.damaged(damage)
            elif p > 0.5:
                return unit.damaged(self.damage)
            else:
                return None
    '''


class Varvar(BaseUnit):
    radius_dmg: float = 8
    base_speed: int = 2
    dmg_coef: float = 2.5

    '''
        def attack(self, map1: Point, unit: BaseUnit) -> int | None:
        dist = unit.coord - self.coord
        in_radius = abs(dist.x) < self.radius_dmg and abs(dist.y) < self.radius_dmg
        if not in_radius:
            self.move_to(unit, map1, 3)
            dist = unit.coord - self.coord
        if abs(dist.x) < self.radius_dmg and abs(dist.y) < self.radius_dmg:
            p = random.random()
            if p > self.p_crit:
                damage = self.damage * 2.5
                return unit.damaged(damage)
            elif p > 0.5:
                return unit.damaged(self.damage)
            else:
                return None
    '''


class Army(BaseModel):
    id: int
    name: str
    count: int
    units: dict[int, Warrior | Archer | Varvar] = dict()

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