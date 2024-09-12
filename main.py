import random
import sys
import json

from pydantic import BaseModel
from logging import StreamHandler
from loguru import logger

from models import Point, Warrior, Archer, Varvar, Army

logger.add("debug.log", format="{time} {level} {message}", level="ERROR")

def main():
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
    while w1 > 0:
        ind = random.randint(0, len(wariors) - 1)
        army1.units[wariors[ind].id] = wariors[ind]
        army1.count += 1
        wariors.pop(ind)
        w1 -= 1
    while a1 > 0:
        ind = random.randint(0, len(archers) - 1)
        army1.units[archers[ind].id] = archers[ind]
        army1.count += 1
        archers.pop(ind)
        a1 -= 1
    while v1 > 0:
        ind = random.randint(0, len(varvars) - 1)
        army1.units[varvars[ind].id] = varvars[ind]
        army1.count += 1
        varvars.pop(ind)
        v1 -= 1

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
    while w2 > 0:
        ind = random.randint(0, len(wariors) - 1)
        army2.units[wariors[ind].id] = wariors[ind]
        army2.count += 1
        wariors.pop(ind)
        w2 -= 1
    while a2 > 0:
        ind = random.randint(0, len(archers) - 1)
        army2.units[archers[ind].id] = archers[ind]
        army2.count += 1
        archers.pop(ind)
        a2 -= 1
    while v2 > 0:
        ind = random.randint(0, len(varvars) - 1)
        army2.units[varvars[ind].id] = varvars[ind]
        army2.count += 1
        varvars.pop(ind)
        v2 -= 1


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
                    print("\nArmy 2 won")
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
                    print("\nArmy 1 won")
                    loss_army = army2.model_dump()
                    loss_army['loss'] = army2.count - len(list(army2.units.keys()))
                    loss_army.pop('count')
                    loss_army.pop('units')
                    res_data = {"win": result_army, "loss": loss_army}
                    with open("res_data.json", 'w') as json_file:
                        json.dump(res_data, json_file)
                print('Some')
                return
            logger.error(e)

        res = army1.units[army1_id].attack(main_map, army2.units[army2_id])
        if res:
            print(f"Unit {army1_id} from army 1 has attacked unit {army2_id} from army 2")
            print(f"Health of unit {army1_id} from army 1: {army1.units[army1_id].health}")
            print(f"Health of unit {army2_id} from army 2: {army2.units[army2_id].health}")
            if res >= 0:
                print(f"Unit {army2_id} has failed")
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
                    print("\nArmy 2 won")
                else:
                    print("\nArmy 1 won")
                return
            logger.error(e)

        res = army2.units[army2_id].attack(main_map, army1.units[army1_id])
        if res:
            print(f"Unit {army2_id} from army 2 has attacked unit {army1_id} from army 1")
            print(f"Health of unit {army2_id} from army 2: {army2.units[army2_id].health}")
            print(f"Health of unit {army1_id} from army 1: {army1.units[army1_id].health}")
            if res >= 0:
                print(f"Unit {army1_id} has failed")
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
            result_army = army2.model_dump()
            result_army['loss'] = army2.count - len(list(army2.units.keys()))
            result_army.pop('count')
            result_army.pop('units')
            print("\nArmy 2 won")
            loss_army = army1.model_dump()
            loss_army['loss'] = army1.count - len(list(army1.units.keys()))
            loss_army.pop('count')
            loss_army.pop('units')
            res_data = {"win": result_army, "loss": loss_army}
            with open("res_data.json", 'w') as json_file:
                json.dump(res_data, json_file)
        elif not keys2:
            result_army = army1.model_dump()
            result_army['loss'] = army1.count - len(list(army1.units.keys()))
            result_army.pop('count')
            result_army.pop('units')
            print("\nArmy 1 won")
            loss_army = army2.model_dump()
            loss_army['loss'] = army2.count - len(list(army2.units.keys()))
            loss_army.pop('count')
            loss_army.pop('units')
            res_data = {"win": result_army, "loss": loss_army}
            with open("res_data.json", 'w') as json_file:
                json.dump(res_data, json_file)


if __name__ == "__main__":
    main()