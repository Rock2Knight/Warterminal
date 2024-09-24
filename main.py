import random
import sys
import json
import asyncio
from logging import StreamHandler
from loguru import logger

from pydantic import BaseModel
from fastapi import FastAPI
from tortoise.filters import Filter

from schemas import *
from models import *
from controllers import *
import crud

logger.add("debug.log", format="{time} {level} {message}", level="INFO")

app = FastAPI()


async def attack(attack_info: AttackDto, victim_unit: AbstractUnit):
    dist = victim_unit.coord - self.coord
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


async def mass_attack(units_of_army: dict[str, list[BaseUnit]]):

    for type_of_army, units in units_of_army.items():
        id_attack = random.randint(0, len(units)-1)


async def fight(army1: Army, army2: Army):
    """ Тут уже сама  """


def match_rival(army_id: int, army: Army, id_list: list, army_in_figths: set) -> tuple[army]:
    fight_with = i
    is_found_victim = False
    res_rivals = None
    while fight_with == i and not is_found_victim:
        fight_with = random.choice(id_list)

        async def wrap_match(fight_with: int, army_in_figths: set) -> Optional[tuple[Army]]:
            res_rivals = None
            if fight_with != i:
                army_to_fight = await crud.get_army_by_id(army_id=fight_with)
                if army_to_fight not in army_in_figths:
                    army_to_fight = await crud.update_army_status(army_id=army_to_fight.id, figths_with=army.id)
                    army = await crud.update_army_status(army_id=army.id, figths_with=army_to_fight.id)
                    res_rivals = (army, army_to_fight)
                    return res_rivals    

        new_loop = asyncio.new_event_loop()
        new_loop.run_until_complete()

        if fight_with != i:
            army_to_fight = await crud.get_army_by_id(army_id=fight_with)
            if army_to_fight not in army_in_figths:
                army_to_fight = await crud.update_army_status(army_id=army_to_fight.id, figths_with=army.id)
                army = await crud.update_army_status(army_id=army.id, figths_with=army_to_fight.id)
                res_rivals = (army, army_to_fight)
                is_found_victim = True
    
    return res_rivals


async def play(game: Game) -> Game:
    if not game.is_play:
        return game

    army_cnt_list = list([])
    armies = await Army.all().order_by('id')
    army_in_figths = set()                   # Армии, которые находятся в бою
    id_list = [army.id for army in armies]   # Список id армий

    while len(armies) > 1:
        # Цикл организации сражений

        for i, army in enumerate(armies):
            # Поиск соперника для армии

            if army not in army_in_figths:
                id_list = [army.id for army in armies]  
                army, army_to_fight = match_rival(i, army, id_list, army_in_figths)  # Подбор армии-соперника
                armies[i], armies[army.fight_with_id] = army, army_to_fight              # Обновляем данные об армиях
                army_in_figths.add(army)                                      # Помечаем армии, как "в бою"
                army_in_figths.add(army_to_fight)
                await fight(army, army_to_fight)               # БИТВА!
            else:
                # Если армия не в бою
                if not is_exist_army(army.fight_with_id):    # Проверка сущствования армии-соперника в базе
                    id_list = [army.id for army in armies]
                    army_in_figths.remove(army)              # Убираем у армии метку "в бою"
                    army, army_to_fight = match_rival(i, army, id_list, army_in_figths) # Подбираем НОВОГО соперника для армии
                    armies[i], armies[army.fight_with_id] = army, army_to_fight   # Сохраняем обновленные версии армий из пары в списке армий
                    army_in_figths.add(army)                 # Помечаем армии как в бою
                    army_in_figths.add(army_to_fight)
                    await fight(army, army_to_fight)               # БИТВА!
                if not army.fight_with_id:                   # Если армия до сих пор ни с кем не сражалсь
                    potential_rivals = crud.get_free_armies(army.id)  # Ищем потенциальных соперников
                    if potential_rivals:
                        # Если они есть
                        id_list = [rival.id for rival in potential_rivals]
                        army, army_to_fight = match_rival(i, army, id_list, army_in_figths) # Подбираем соперника для армии
                        armies[i], armies[army.fight_with_id] = army, army_to_fight              # Обновляем данные об армиях
                        army_in_figths.add(army)                                      # Помечаем армии, как "в бою"
                        army_in_figths.add(army_to_fight)
                        await fight(army, army_to_fight)               # БИТВА!



@app.get("/")
async def read_root():
    # Тестовая запрос
    return {"Hello": "World"}


@app.post("/game/{army_count}/{units_count}")
def start_game(army_count: int, units_count: int, game: Game):
    unit_id = 1

    #--------------------------------------------------------------
    # Заполняем базу начальными значениями

    for army in game.armies:
        await Army.create(id=army.id, name=army.name, count=army.count) # Добавляем армию в базу
        for unit in army.units:
            # Формируем данные для каждого юнита армии
            type_unit = None

            # Тип юнита
            match unit.unit_type:
                case unit.unit_type.Warior:
                    type_unit = 0
                case unit.unit_type.Archer:
                    type_unit = 1
                case unit.unit_type.Varvar:
                    type_unit = 2
            unit_health, unit_damage, unit_defense = 100.0, 10.0, 50.0  # Дефолтные значения здоровья, атаки, защиты

            # Ставим введенные значения, если они есть
            if unit.health:
                unit_health = unit_health
            if unit.damage:
                unit_damage = unit.damage
            if unit.defene:
                unit_defense = unit.defense

            # Добавляем юнита в базу
            await Unit.create(id=unit_id, typeunit_id=type_unit, army_id=army.id,
                x_coord=unit.coord.x, y_coord=unit.coord.y, health=unit_health,
                damage=unit_damage, defense=unit_defense)
            unit_id += 1                                  # Инкрементируем id для следующей записи
    


    #return {"army_name": army.name, "army_id": army.id, "army_count": army.count}

'''


async def main():
    main_map = Point(x=30, y=30)
    print("Enter count of characters: ")
    wariors = list([])
    archers = list([])
    varvars = list([])
    cur_id = 1
    count = int(input())

    for _ in range(count):
        # Вводим координаты юнитов
        X = random.randint(1, main_map.x)
        Y = random.randint(1, main_map.y)
        pnt = Point(x=X, y=Y)
        t1 = pnt.x > 0 and pnt.x < main_map.x
        t2 = pnt.y > 0 and pnt.y < main_map.y
        while not t1 and not t2:
            X = random.randint(1, main_map.x)
            Y = random.randint(1, main_map.y)
            pnt = Point(x=X, y=Y)
            t1 = pnt.x > 0 and pnt.x < main_map.x
            t2 = pnt.y > 0 and pnt.y < main_map.y
        print("Enter type of character (w/a/v):", end=' ')
        s = random.choice(['w', 'a', 'v'])

        match s:         # Создаем списки юнитов
            case 'w':
                wariors.append(Warrior(id=cur_id, coord=pnt))
                cur_id += 1
            case 'a':
                archers.append(Archer(id=cur_id, coord=pnt))
                cur_id += 1
            case 'v':
                varvars.append(Varvar(id=cur_id, coord=pnt))
                cur_id += 1

    # Вводим данные для 1-ой армии
    print("Enter number of warriors in 1st army: ")
    w1 = 5
    print("Enter number of archers in 1st army: ")
    a1 = 3
    print("Enter number of varvars in 1st army: ")
    v1 = 4

    print("Enter name of army 1: ", end=' ')
    army1_name = input()

    army1 = Army(id=1, name=army1_name, count=0, units=dict())

    # Добавляем юнитов в 1-ую армию
    army1.add_unit(w1, wariors)
    army1.add_unit(a1, archers)
    army1.add_unit(v1, varvars)

    # Вводим данные для 2-ой армии
    print("Enter number of warriors in 2st army: ")
    w2 = 4
    print("Enter number of archers in 2st army: ")
    a2 = 4
    print("Enter number of varvars in 2st army: ")
    v2 = 4

    print("Enter name of your army: ", end=" ")
    army2_name = input()

    army2 = Army(id=2, name=army2_name, count=0, units=dict())

    # Добавляем юнитов в 2-ую армию
    army2.add_unit(w2, wariors)
    army2.add_unit(a2, archers)
    army2.add_unit(v2, varvars)

    while len(list(army1.units.keys())) > 0 and len(list(army2.units.keys())) > 0:
        keys1 = list(army1.units.keys())
        keys2 = list(army2.units.keys())

        try:
            army1_id = random.choice(keys1)
            army2_id = random.choice(keys2)
        except IndexError:
            if not keys1 or not keys2:
                if not keys1:
                    result_army = army2.model_dump()
                    result_army['loss'] = army2.count - len(list(army2.units.keys()))
                    result_army.pop('count')
                    result_army.pop('units')
                    logger.info("\nArmy 2 won")
                    loss_army = army1.model_dump()
                    loss_army['loss'] = army1.count - len(list(army1.units.keys()))
                    loss_army.pop('count')
                    loss_army.pop('units')
                    res_data = {"win": result_army, "loss": loss_army}
                    with open("res_data.json", 'w') as json_file:
                        json.dump(res_data, json_file)
                else:
                    result_army = army1.model_dump()
                    result_army['loss'] = army1.count - len(list(army1.units.keys()))
                    result_army.pop('count')
                    result_army.pop('units')
                    logger.info("\nArmy 1 won")
                    loss_army = army2.model_dump()
                    loss_army['loss'] = army2.count - len(list(army2.units.keys()))
                    loss_army.pop('count')
                    loss_army.pop('units')
                    res_data = {"win": result_army, "loss": loss_army}
                    with open("res_data.json", 'w') as json_file:
                        json.dump(res_data, json_file)
                return
            logger.error(e)

        res = await army1.units[army1_id].attack(main_map, army2.units[army2_id])
        if res:
            logger.info(f"Unit {army1_id} from {army1.name} has attacked unit {army2_id} from {army2.name}")
            logger.info(f"Health of unit {army1_id} from {army1.name}: {army1.units[army1_id].health}")
            logger.info(f"Health of unit {army2_id} from {army2.name}: {army2.units[army2_id].health}")
            if res >= 0:
                logger.info(f"Unit {army2_id} has failed")
                army2.units.pop(army2_id)

        move_x = random.randint(-army1.units[army1_id].coord.x, main_map.x - army1.units[army1_id].coord.x)
        move_y = random.randint(-army1.units[army1_id].coord.y, main_map.y - army1.units[army1_id].coord.y)

        move_p = Point(x=move_x, y=move_y)
        army1.units[army1_id].coord = army1.units[army1_id].coord + move_p

        if army2_id in army2.units.keys():
            move_x = random.randint(-army2.units[army2_id].coord.x, main_map.x - army2.units[army2_id].coord.x)
            move_y = random.randint(-army2.units[army2_id].coord.y, main_map.y - army2.units[army2_id].coord.y)

            move_p = Point(x=move_x, y=move_y)
            army2.units[army2_id].coord = army2.units[army2_id].coord + move_p

        # *******************************************************

        keys1 = list(army1.units.keys())
        keys2 = list(army2.units.keys())

        try:
            army1_id = random.choice(keys1)
            army2_id = random.choice(keys2)
        except IndexError as e:
            if not keys1 or not keys2:
                if not keys1:
                    await output(army2, army1)
                else:
                    await output(army1, army2)
                return
            logger.error(e)

        res = await army2.units[army2_id].attack(main_map, army1.units[army1_id])
        if res:
            logger.info(f"Unit {army2_id} from {army2.name} has attacked unit {army1_id} from {army1.name}")
            logger.info(f"Health of unit {army2_id} from {army2.name}: {army2.units[army2_id].health}")
            logger.info(f"Health of unit {army1_id} from {army1.name}: {army1.units[army1_id].health}")
            if res >= 0:
                logger.info(f"Unit {army1_id} has failed")
                army1.units.pop(army1_id)

        try:
            move_x = random.randint(-army2.units[army2_id].coord.x, main_map.x - army2.units[army2_id].coord.x)
            move_y = random.randint(-army2.units[army2_id].coord.y, main_map.y - army2.units[army2_id].coord.y)
        except Exception as e:
            logger.exception(e)

        move_p = Point(x=move_x, y=move_y)
        army2.units[army2_id].coord = army2.units[army2_id].coord + move_p

        if army1_id in army1.units.keys():
            move_x = random.randint(-army1.units[army1_id].coord.x, main_map.x - army1.units[army1_id].coord.x)
            move_y = random.randint(-army1.units[army1_id].coord.y, main_map.y - army1.units[army1_id].coord.y)

            move_p = Point(x=move_x, y=move_y)
            army1.units[army1_id].coord = army1.units[army1_id].coord + move_p

        keys1 = list(army1.units.keys())
        keys2 = list(army2.units.keys())
        if not keys1:
            await output(army2, army1)
        elif not keys2:
            await output(army1, army2)


if __name__ == "__main__":
    asyncio.run(main())
'''
