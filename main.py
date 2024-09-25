import random
import sys
import json
import asyncio
import math
import time

from logging import StreamHandler
from loguru import logger

from pydantic import BaseModel
from fastapi import FastAPI
from tortoise.exceptions import IntegrityError

from schemas import *
from models import *
from controllers import *
import crud

logger.add("debug.log", format="{time} {level} {message}", level="INFO")

app = FastAPI()


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


            if army in army_in_figths:
                # Если армия была в бою
                is_exist_army = await crud.is_exist_army(army.fight_with_id)
                if not is_exist_army:    # Проверка сущствования армии-соперника в базе
                    army_in_figths.remove(army)              # Убираем у армии метку "в бою"

            id_list = [army.id for army in armies] 
            res_match = match_rival(i, army, id_list, army_in_figths)  # Подбор армии-соперника
            if res_match:
                army, army_to_fight = res_match
            else:
                continue
            armies[i], armies[army.fight_with_id] = army, army_to_fight              # Обновляем данные об армиях
            army_in_figths.add(army)                                      # Помечаем армии, как "в бою"
            army_in_figths.add(army_to_fight)
            await fight(army, army_to_fight, game.gmap, timeout=120)               # БИТВА!
        
        armies = await Army.all().order_by('id')

    win_army = await Army.all().first()
    win_units = crud.get_army_units(win_army.id)
    win_army_stat: ArmyStatBase = ArmyStatBase(id=win_army.id, name=win_army.name, loss=win_army.count-len(win_units))
    game.win_army = win_army_stat
    game.is_play = False
    return game


@app.get("/")
async def read_root():
    # Тестовая запрос
    return {"Hello": "World"}


@app.post("/game/{army_count}/{units_count}")
async def start_game(army_count: int, units_count: int, game: Game):
    model_dump = game.model_dump()
    print(model_dump)

    warrior_id, archer_id, varvar_id = 1, 1, 1
    print('\n\n')
    for army in game.armies:
        print(army, '\n')

    #--------------------------------------------------------------
    # Заполняем базу начальными значениями

    for army in game.armies:
        print(f'\nArmy: {army.name}')
        print("Units:")
        print(army.units)

        try:
            await Army.create(id=army.id, name=army.name, count=army.count) # Добавляем армию в базу
        except Exception as e:
            logger.error(e)


        for unit in army.units.values():
            # Формируем данные для каждого юнита армии
            type_unit = None
            unit_health, unit_damage, unit_defense = 100.0, 10.0, 50.0  # Дефолтные значения здоровья, атаки, защиты

            # Ставим введенные значения, если они есть
            if unit.health:
                unit_health = unit_health
            if unit.damage:
                unit_damage = unit.damage
            if unit.defense:
                unit_defense = unit.defense

            # Добавляем юнита в базу
            match unit.dto_name:
                case "Warrior":
                    await Warrior.create(id=warrior_id, army_id=army.id,
                        x_coord=unit.coord.x, y_coord=unit.coord.y, health=unit_health,
                        damage=unit_damage, defense=unit_defense)
                    warrior_id += 1
                case "Archer":
                    await Archer.create(id=archer_id, army_id=army.id,
                        x_coord=unit.coord.x, y_coord=unit.coord.y, health=unit_health,
                        damage=unit_damage, defense=unit_defense)
                    archer_id += 1
                case "Varvar":
                    await Varvar.create(id=varvar_id, army_id=army.id,
                        x_coord=unit.coord.x, y_coord=unit.coord.y, health=unit_health,
                        damage=unit_damage, defense=unit_defense)
                    varvar_id += 1


    # --------------------------------------------------------------

    game_result = await play(game)  # Запускаем игру
    return game_result.model_dump()