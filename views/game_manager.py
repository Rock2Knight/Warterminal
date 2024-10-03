import math
import time
from typing import Optional

from loguru import logger
from tortoise.exceptions import IntegrityError

from .imports import *

class GameManager:

    @staticmethod
    async def coord_in_map(unit: AbstractUnit, map1: Point) -> AbstractUnit:
        """ 
        Определение, находится ли юнит в пределах карты
        :param unit:  юнит, для которого определяется находится ли он в пределах карты
        :param map1: размеры карты
        """
        if unit.x_coord < 0:
            unit.x_coord = 1
        elif unit.x_coord > map1.x:
            unit.x_coord = map1.x - 1
        if unit.y_coord < 0:
            unit.y_coord = 1
        elif unit.y_coord > map1.y:
            unit.y_coord = map1.y - 1

        return unit
    
    @classmethod
    async def move_to(cls, attacking_unit: AbstractUnit, victim_unit: AbstractUnit, map1: Point) -> AbstractUnit:
        """ 
        Перемещение атакующего юнита к атакуемому 
        :param attacking_unit: атакующий юнит
        :param victim_unit: юнит, к которому перемещаемся
        :param map1: размеры карты
        :return: атакующий юнит (уже перемещенный)
        """

        logger.info(f"Юнит {attacking_unit.id} передвигается к юниту {victim_unit.id}")
        logger.info(f"Место юнита {attacking_unit.id}: x={attacking_unit.x_coord:.2f}  y={attacking_unit.y_coord:.2f}")

        if victim_unit.x_coord < attacking_unit.x_coord:
            attacking_unit.x_coord = attacking_unit.x_coord - 2
        else:
            attacking_unit.x_coord = attacking_unit.x_coord + 2

        if victim_unit.y_coord < attacking_unit.y_coord:
            attacking_unit.y_coord = attacking_unit.y_coord - 2
        else:
            attacking_unit.y_coord = attacking_unit.y_coord + 2

        attacking_unit = await cls.coord_in_map(attacking_unit, map1)
        try:
            await attacking_unit.save()
        except IntegrityError:
            logger.error(f"Модель не может быть создана или обновлена")
            exit(1)
        logger.success(f"Юнит {attacking_unit.id} переместился к юниту {victim_unit.id}")
        logger.success(f"Место юнита {attacking_unit.id}: x={attacking_unit.x_coord:.2f}  y={attacking_unit.y_coord:.2f}")
        return attacking_unit
    

    @staticmethod
    async def match_rival(army_id: int, army: Army, id_list: list, army_in_figths: set, timeout: int = 3) -> tuple[Army]:
        """ 
        Подбор армии-соперника
        :param army_id:  id армии, для которой подбираем соперника
        :param id_list: список армий кандидатов
        :param army_in_figths: армиии, которые уже в бою

        :return: tuple[Army, Army] - кортеж с армиями-соперниками
        """
        logger.info("Point 3")
        fight_with = army_id      # id потенциального противника
        is_found_victim = False   # найден ли противник
        res_rivals = None         # Кортеж соперников
        checked_id = list([])     # Список id проверенных соперников

        # засекаем таймер, чтобы избежать простаивания
        t1 = time.perf_counter()
        t2 = time.perf_counter()
        prev_diff = t2 - t1

        while fight_with == army_id and not is_found_victim:   # Пока жертва не найдена
            fight_with = random.choice(id_list)                # Выбираем случайную армию-соперника

            army_debug1 = await get_army_by_id(army_id=fight_with)  # Армия, для которой мы подбираем противника
            army_debug2 = await get_army_by_id(army_id=fight_with)  # Потенциальный противник

            logger.info(f"id={army_debug1.id}, content={dict(army_debug1)}")
            logger.info(f"id={army_debug2.id}, content={dict(army_debug2)}")

            if fight_with != army_id:                          # Если мы не выбрали нашу армию

                logger.info("Before get army by id")
                army_to_fight = await get_army_by_id(army_id=fight_with) # Получаем потенциальную армию-соперника
                logger.info(f"id={army_to_fight.id}, name={army_to_fight.name} type={type(army_to_fight)}")  # (1)

                if army_to_fight not in army_in_figths:
                    # Если потенциальный соперник не в бою
                    # Устанавливаем поле id соперника для каждого соперника
                    army_to_fight = await update_army_status(army_id=army_to_fight.id, figths_with=army.id)
                    army = await update_army_status(army_id=army.id, figths_with=army_to_fight.id)
                    res_rivals = (army, army_to_fight, army_in_figths)  # Кортеж соперников
                    is_found_victim = True   # Отмечаем, что нашли противника

            if not fight_with in checked_id:          # Если id потенциального соперника не в списке проверенных
                logger.info(f"Army {fight_with} not in checked id list")
                checked_id.append(fight_with)   # Добавляем id потенциального соперника в список проверенных
                logger.info(f"Армия {fight_with} добавлена в список проверенных")
            if len(checked_id) >= len(id_list) and not is_found_victim: 
                logger.info("A victim is not found")
                return None   # Если не нашли противника, возвращаем None
            
            # Фиксируем время выполнения
            t2 = time.perf_counter()
            diff = t2 - t1
            if diff - prev_diff >= 1:
                logger.info(f"Time of executing: {diff:.3f} sec")
                prev_diff = diff
            if diff > timeout:
                raise TimeoutError     # Выход из метода, если он завис
        
        return res_rivals
    

    @staticmethod
    async def delete_with_log_unit(unit: AbstractUnit, army: Army):
        """ 
        Удаление юнита из БД с выводом результата 
        """

        logger.info(f"Unit {unit.id} from {army.name} has failed")
        if isinstance(unit, Warrior):
            await delete_warrior(unit.id)
        elif isinstance(unit, Archer):
            await delete_archer(unit.id)
        elif isinstance(unit, Varvar):
            await delete_varvar(unit.id)
        else:
            logger.error("Неизвестный тип юнита")
            raise UndefinedUnitTypeException("Неизвестный тип юнита")
        logger.success(f"Unit {unit.id} from {army.name} has been deleted")