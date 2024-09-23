import random
import sys
import json
import asyncio

from pydantic import BaseModel
from logging import StreamHandler
from loguru import logger

from models import Point, Warrior, Archer, Varvar, Army

logger.add("debug.log", format="{time} {level} {message}", level="INFO")


async def output(army_win: Army, army_fail: Army):

    result_army = army_win.model_dump()
    result_army['loss'] = army_win.count - len(list(army_win.units.keys()))
    result_army.pop('count')
    result_army.pop('units')
    print("\n")
    logger.info(f"Army {army_win.name} won")
    print("\n")
    loss_army = army_fail.model_dump()
    loss_army['loss'] = army_fail.count - len(list(army_fail.units.keys()))
    logger.info(f"Loss: {loss_army['loss']}")
    loss_army.pop('count')
    loss_army.pop('units')
    res_data = {"win": result_army, "loss": loss_army}
    with open("res_data.json", 'w') as json_file:
        json.dump(res_data, json_file)


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