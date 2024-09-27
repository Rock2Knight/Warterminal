import random
import sys
import json
import asyncio
import math
import time
from contextlib import asynccontextmanager

from logging import StreamHandler
from loguru import logger

from pydantic import BaseModel
from fastapi import FastAPI
from tortoise.exceptions import IntegrityError
from tortoise.transactions import atomic
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

from database.db import DB_CONFIG
from schemas import *
from models import *
from controllers import *
import crud


logger.add("debug.log", format="{time} {level} {message}", level="INFO")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Подключение и инициализация схем при старте
    register_tortoise(
        app,
        config=DB_CONFIG,
        generate_schemas=True,  # Автоматическое создание схем при старте
        add_exception_handlers=True,  # Добавляем обработчики ошибок для Tortoise
    )

@app.on_event("shutdown")
async def shutdown_event():
    # Закрытие соединений при завершении работы приложения
    await Tortoise.close_connections()


async def play(game: Game) -> Game:
    if not game.is_play:
        return game

    army_cnt_list = list([])
    armies_list = await Army.all().order_by('id')
    armies = dict()
    for army in armies_list:
        armies[army.id] = army

    army_in_figths = set()                   # Армии, которые находятся в бою
    id_list = list(armies.keys())   # Список id армий
    logger.info("Point 1")

    while len(armies) > 1:
        # Цикл организации сражений
        #fight_tasks = list([])

        for id, army in armies.items():
            # Поиск соперника для армии

            if army in army_in_figths:
                # Если армия была в бою
                is_exist_army = await crud.is_exist_army(army.fight_with_id)
                if not is_exist_army:    # Проверка сущствования армии-соперника в базе
                    army_in_figths.remove(army)              # Убираем у армии метку "в бою"

            id_list = [id for army in armies] 
            res_match = await match_rival(id, army, id_list, army_in_figths)  # Подбор армии-соперника
            if res_match:
                army, army_to_fight = res_match
            else:
                continue
            armies[id], armies[army.fight_with_id] = army, army_to_fight              # Обновляем данные об армиях
            army_in_figths.add(army)                                      # Помечаем армии, как "в бою"
            army_in_figths.add(army_to_fight)
            #fight_tasks.append(asyncio.create_task(fight(army, army_to_fight, game.gmap, logger, timeout=120)))
            w_army = await fight(army, army_to_fight, game.gmap, timeout=120)               # БИТВА!
        
        #done, pending = asyncio.wait(fight_tasks)
        armies = await Army.all().order_by('id')
        #fight_tasks.clear()

    win_army = await Army.all().first()
    win_units = await crud.get_army_units(win_army.id)
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

    #--------------------------------------------------------------
    # Заполняем базу начальными значениями

    for army in game.armies:

        if army is None:
            raise Exception("Army is None")
    

        new_army = await Army.create(name=army.name, count=army.count) # Добавляем армию в базу

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
                    await Warrior.create(army_id=new_army.id,
                        x_coord=unit.coord.x, y_coord=unit.coord.y, health=unit_health,
                        damage=unit_damage, defense=unit_defense)
                case "Archer":
                    await Archer.create(army_id=new_army.id,
                        x_coord=unit.coord.x, y_coord=unit.coord.y, health=unit_health,
                        damage=unit_damage, defense=unit_defense)
                case "Varvar":
                    await Varvar.create(army_id=new_army.id,
                        x_coord=unit.coord.x, y_coord=unit.coord.y, health=unit_health,
                        damage=unit_damage, defense=unit_defense)


    # --------------------------------------------------------------

    game_result = await play(game)  # Запускаем игру
    return game_result.model_dump()