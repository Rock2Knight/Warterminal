import math
import time
from typing import Optional

from loguru import logger

from tortoise.exceptions import IntegrityError

from numba import jit

from schemas import *
from models import *
import crud

async def coord_in_map(unit: AbstractUnit, map1: Point) -> AbstractUnit:
    if unit.x_coord < 0:
        unit.x_coord = 1
    elif unit.x_coord > map1.x:
        unit.x_coord = map1.x - 1
    if unit.y_coord < 0:
        unit.y_coord = 1
    elif unit.y_coord > map1.y:
        unit.y_coord = map1.y - 1

    return unit


async def match_rival(army_id: int, army: Army, id_list: list, army_in_figths: set, timeout: int = 10) -> Optional[tuple[Army]]:
    """ 
    Подбор армии-соперника
    :param army_id:  id армии, для которой подбираем соперника
    :param id_list: список армий кандидатов
    :param army_in_figths: армиии, которые уже в бою

    :return: tuple[Army, Army] - кортеж с армиями-соперниками
    """

    logger.info("Point 3")
    fight_with = army_id
    is_found_victim = False
    res_rivals = None
    checked_id = list([])
    t1 = time.perf_counter()
    t2 = time.perf_counter()
    prev_diff = t2 - t1
    while fight_with == army_id and not is_found_victim:
        fight_with = random.choice(id_list)
        if fight_with != army_id:
            logger.info("Before get army by id")
            army_to_fight = await crud.get_army_by_id(army_id=fight_with) # Получаем потенциальную армию-соперника
            logger.info(f"id={army_to_fight}, type={type(army_to_fight)}")  # (1)
            if army_to_fight not in army_in_figths:
                # Если потенциальный соперник не в бою
                # Устанавливаем поле id соперника для каждого соперника
                army_to_fight = await crud.update_army_status(army_id=army_to_fight.id, figths_with=army.id)
                army = await crud.update_army_status(army_id=army.id, figths_with=army_to_fight.id)
                res_rivals = (army, army_to_fight)  # Кортеж соперников
                is_found_victim = True   # Отмечаем, что нашли противника
        if not fight_with in checked_id:
            logger.info("Id in checked id list")
            checked_id.append(fight_with)   # Добавляем id потенциального соперника в список проверенных
        if len(checked_id) >= len(id_list) and not is_found_victim: 
            logger.info("A victim is not found")
            return None   # Если не нашли противника, возвращаем None
        t2 = time.perf_counter()
        diff = t2 - t1
        if diff - prev_diff >= 1:
            logger.info(f"Time of executing: {diff:.3f} sec")
            prev_diff = diff
        if diff > timeout:
            return None
    
    return res_rivals


async def move_to(attacking_unit: AbstractUnit, victim_unit: AbstractUnit, map1: Point) -> AbstractUnit:
    """ Перемещение атакующего юнита к атакуемому """

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

    attacking_unit = await coord_in_map(attacking_unit, map1)
    try:
        await attacking_unit.save()
    except IntegrityError:
        logger.error(f"Модель не может быть создана или обновлена")
        exit(1)
    logger.info(f"Юнит {attacking_unit.id} переместился к юниту {victim_unit.id}")
    logger.info(f"Место юнита {attacking_unit.id}: x={attacking_unit.x_coord:.2f}  y={attacking_unit.y_coord:.2f}")
    return attacking_unit


async def damage(unit1: AbstractUnit, unit2: AbstractUnit, is_crit: bool = False) -> Optional[AbstractUnit]:
    """ Логика нанесения урона юниту """

    print("n\n\n")
    logger.info(f"unit1: {unit1}, unit2: {unit2}")
    print("n\n\n")

    dmg = unit1.damage
    if is_crit:
        dmg *= unit1.dmg_coef

    if unit2.health > 0:
        if unit2.defense > 0:
            unit2.health = unit2.health - (dmg - unit2.defense)
            unit2.defense -= 2
        else:
            unit2.health -= dmg
        await unit2.save()
    if unit2.health <= 0:
        return unit2
    return None


async def attack(attacking_unit: AbstractUnit, victim_unit: AbstractUnit, map1: Point) -> bool:
    dist = Point(x=abs(victim_unit.x_coord-attacking_unit.x_coord), y=abs(victim_unit.y_coord-attacking_unit.y_coord))
    in_radius = abs(dist.x) < attacking_unit.radius_dmg and abs(dist.y) < attacking_unit.radius_dmg
    if not in_radius:
        attacking_unit = await move_to(attacking_unit, victim_unit, map1)
        dist = Point(x=abs(victim_unit.x_coord-attacking_unit.x_coord), y=abs(victim_unit.y_coord-attacking_unit.y_coord))
    if math.sqrt(abs(dist.x)**2+abs(dist.y)) < attacking_unit.radius_dmg:
        p = random.choice(list(range(5)))
        match p:
            case 0 | 1: return False
            case 2 | 3:
                victim_unit = await damage(attacking_unit, victim_unit)
                await victim_unit.save()
                return True
            case 4:
                victim_unit = await damage(attacking_unit, victim_unit, is_crit=True)
                await victim_unit.save()
                return True
    return False


async def delete_with_log_unit(unit: AbstractUnit, army: Army):
    """ Удаление юнита из БД с выводом результата """

    logger.info(f"Unit {unit.id} from {army.name} has failed")
    try:
        await crud.delete_unit(unit)
    except ValueError:
        logger.error(f"Не удалось удалить юнита {unit.id} из армии {army.name}")
        exit(1)



async def fight(army1: Army, army2: Army, map1: Point, logger, timeout: int = 1000000):
    """ Тут уже сама логика битвы"""
    is_first = True

    units1 = await crud.get_army_units(army1.id)
    units2 = await crud.get_army_units(army2.id)
    is_attacked: bool = False

    t1 = time.perf_counter()    # Засекаем время для задержки

    # Логика сражения
    while len(units1 > 0) and len(units2) > 0:
        logger.info(f"Количество юнитов в армии {army1.name} = {len(units1)}")
        logger.info(f"Количество юнитов в армии {army2.name} = {len(units2)}")
        army1_unit = random.choice(units1)
        army2_unit = random.choice(units2)

        if is_first:
            is_attacked = await attack(army1_unit, army2_unit, map1)
        else:
            is_attacked = await attack(army2_unit, army1_unit, map1)

        if is_attacked:
            try:
                army1_unit = await crud.get_concrete_unit(army1_unit)
            except ValueError as ve:
                logger.error(f"Неизвестный тип юнита: {type(army1_unit)}")
                exit(1)

            try:
                army2_unit = await crud.get_concrete_unit(army2_unit)
            except ValueError as ve:
                logger.error(f"Неизвестный тип юнита: {type(army2_unit)}")
                exit(1)

            # Вывод информации о состоянии игроков
            if is_first:
                logger.info(f"Unit {army1_unit.id} from {army1.name} has attacked unit {army2_unit.id} from {army2.name}")
            else:
                logger.info(f"Unit {army2_unit.id} from {army2.name} has attacked unit {army1_unit.id} from {army1.name}")

            logger.info(f"Health of unit {army1_unit.id} from {army1.name}: {army1_unit.health}")
            logger.info(f"Health of unit {army2_unit.id} from {army2.name}: {army2_unit.health}")

            # Удаление юнита из БД, если он умер (а также вывод информации о падшем бойце)
            if is_first and army2_unit.health <= 0:
                await delete_with_log_unit(army2_unit, army2)
            elif not is_first and army1_unit.health <= 0:
                await delete_with_log_unit(army1_unit, army1)

        # Обновляем списки юнитов для каждой армии
        units1 = await crud.get_army_units(army1.id)
        units2 = await crud.get_army_units(army2.id)
        is_first = not is_first                       # Меняем очередность хода

        t2 = time.perf_counter()
        t_diff = t2 - t1 # Проверка задержки
        if t_diff > timeout:
            logger.info(f"Timeout for fight {army1.name} VS {army2.name}")
            return
        
    if units1 and not units2:
        army1 = await Army.filter(id=army1.id).first()
        army1.fight_with_id = None
        await army1.save()
        del_army = await Army.filter(id=army2.id).delete()
        logger.info(f"Army {del_army.name} with id {del_army.id} was deleted")
        return army1
    elif not units1 and units2:
        army2 = await Army.filter(id=army2.id).first()
        army2.fight_with_id = None
        await army2.save()
        del_army = await Army.filter(id=army1.id).delete()
        logger.info(f"Army {del_army.name} with id {del_army.id} was deleted")
        return army2
    else:
        raise ValueError("Недействительный исход боя")