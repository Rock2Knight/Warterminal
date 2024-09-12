import random
from abc import abstractmethod

from pydantic import BaseModel


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
    p_crit: float
    radius_dmg: int

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


    def move_to(self, unit, map1: Point, speed: int = 1):
        p_move = random.random()
        x_move, y_move = False, False
        if abs(unit.coord.x - self.coord.x) > abs(unit.coord.y - self.coord.y):
            x_move = True
        else:
            y_move = True

        p_move = random.random()
        if p_move < 0.2:
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
        elif p_move < 0.4:
            if x_move:
                if unit.coord.x < self.coord.x:
                    self.coord.x = self.coord.x - 4 * speed
                else:
                    self.coord.x = self.coord.x + 4 * speed
            else:
                if unit.coord.y < self.coord.y:
                    self.coord.y = self.coord.y - 4 * speed
                else:
                    self.coord.y = self.coord.y + 4 * speed
        elif p_move < 0.6:
            if x_move:
                if unit.coord.x < self.coord.x:
                    self.coord.x = self.coord.x - 8 * speed
                else:
                    self.coord.x = self.coord.x + 8 * speed
            else:
                if unit.coord.y < self.coord.y:
                    self.coord.y = self.coord.y - 8 * speed
                else:
                    self.coord.y = self.coord.y + 8 * speed
        elif p_move < 0.8:
            if x_move:
                if unit.coord.x < self.coord.x:
                    self.coord.x = self.coord.x - 12 * speed
                else:
                    self.coord.x = self.coord.x + 12 * speed
            else:
                if unit.coord.y < self.coord.y:
                    self.coord.y = self.coord.y - 12 * speed
                else:
                    self.coord.y = self.coord.y + 12 * speed
        else:
            if x_move:
                if unit.coord.x < self.coord.x:
                    self.coord.x = self.coord.x - 15 * speed
                else:
                    self.coord.x = self.coord.x + 15 * speed
            else:
                if unit.coord.y < self.coord.y:
                    self.coord.y = self.coord.y - 15 * speed
                else:
                    self.coord.y = self.coord.y + 15 * speed

        if self.coord.x < 0:
            self.coord.x = 1
        elif self.coord.x > map1.x:
            self.coord.x = map1.x - 1
        if self.coord.y < 0:
            self.coord.y = 1
        elif self.coord.y > map1.y:
            self.coord.y = map1.y - 1


class Warrior(BaseUnit):
    p_crit: float = 0.7
    radius_dmg: float = 10

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


class Archer(BaseUnit):
    p_crit: float = 0.85
    radius_dmg: float = 20

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


class Varvar(BaseUnit):
    p_crit: float = 0.9
    radius_dmg: float = 8

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


class Army(BaseModel):
    id: int
    name: str
    count: int
    units: dict[int, Warrior | Archer | Varvar] = dict()