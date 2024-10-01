import math
import time
import pickle
from typing import Optional

from loguru import logger
from tortoise.exceptions import IntegrityError
from fastapi.exceptions import HTTPException

from .imports import *

class Fight:

    @staticmethod
    async def _damage(unit1: AbstractUnit, unit2: AbstractUnit, is_crit: bool = False) -> Optional[AbstractUnit]:
        """
        Логика нанесения урона юниту
        :param unit1: первый юнит (атакующий)
        :param unit2: второй юнит (который защищается)
        :param is_crit: флаг определения урона
        :return: обновленные данные о защищаюсемся юните
        """
        pass


    @classmethod
    async def _attack(cls, attacking_unit: AbstractUnit, victim_unit: AbstractUnit, map1: Point) -> bool:
        """
        Логика атаки
        :param attacking_unit: атакующий юнит
        :param victim_unit: противник
        :param map1: размеры карты
        :return: результат атаки
        """
        logger.success(f"Юнит {attacking_unit.id} по имени {attacking_unit.name} пошел с мечом" +
                f"на {victim_unit.id} юнита по имени {victim_unit.name}")
        
        dist = Point(x=abs(victim_unit.x_coord-attacking_unit.x_coord), y=abs(victim_unit.y_coord-attacking_unit.y_coord))
        in_radius = abs(dist.x) < attacking_unit.radius_dmg and abs(dist.y) < attacking_unit.radius_dmg

        if not in_radius:
            try:
                attacking_unit = await GameManager.move_to(attacking_unit, victim_unit, map1)
            except Exception as e:
                raise e
            else:
                logger.success(f"Юнит {attacking_unit.id} приблизился к юниту {victim_unit.id}")

            dist = Point(x=abs(victim_unit.x_coord-attacking_unit.x_coord), y=abs(victim_unit.y_coord-attacking_unit.y_coord))
        if math.sqrt(abs(dist.x)**2+abs(dist.y)**2) < attacking_unit.radius_dmg:
            logger.info(f"Жертва в зоне поражения юнита {attacking_unit.id}")
            p = random.choice(list(range(5)))
            match p:
                case 0 | 1: return False
                case 2 | 3:
                    victim_unit = await cls._damage(attacking_unit, victim_unit)
                    await victim_unit.save()
                    return True
                case 4:
                    victim_unit = await cls._damage(attacking_unit, victim_unit, is_crit=True)
                    await victim_unit.save()
                    return True
        return False



    @classmethod
    async def _fight_process(cls, army1: Army, army2: Army, map1: Point, timeout: int = 120) -> Optional[Army]:
        """
        Логика битвы между двумя армиями
        :param army1: первая армия
        :param army2: вторая армия
        :param map1: размеры карты
        :param timeout: время ожидания в секундах
        :return: Выигравшая сторона
        """
        logger.success(f"Запущена битва между армией {army1.id} и армией {army2.id}")

        is_first = True      # Атакует первая/вторая сторона

        units1 = await get_army_units(army1.id)
        units2 = await get_army_units(army2.id)
        is_attacked: bool = False                # Была ли атакована армия

        t1 = time.perf_counter()    # Засекаем время для задержки

        # Логика сражения: сражаемся пока стороны не перебьют друг друга ИЛИ не истечет таймер
        while len(units1 > 0) and len(units2) > 0:
            logger.info(f"Количество юнитов в армии {army1.name} = {len(units1)}")
            logger.info(f"Количество юнитов в армии {army2.name} = {len(units2)}")
            army1_unit = random.choice(units1)
            army2_unit = random.choice(units2)

            if is_first:
                is_attacked = await cls._attack(army1_unit, army2_unit, map1)  # Если очередь атакующей стороны, то атакует она
            else:
                is_attacked = await cls._attack(army2_unit, army1_unit, map1)  # Иначе отвечает защищаюсяя

            if is_attacked:
                try:
                    army1_unit = await get_concrete_unit(army1_unit)
                except ValueError as ve:
                    logger.error(f"Неизвестный тип юнита: {type(army1_unit)}")
                    exit(1)

                try:
                    army2_unit = await get_concrete_unit(army2_unit)
                except ValueError as ve:
                    logger.error(f"Неизвестный тип юнита: {type(army2_unit)}")
                    exit(1)

                # Вывод информации о состоянии игроков
                if is_first:
                    logger.info(f"Unit {army1_unit.id} from {army1.name} has attacked unit {army2_unit.id} from {army2.name}")
                    logger.success(f"Unit {army1_unit.id} from {army1.name} has damaged unit {army2_unit.id} from {army2.name}")
                else:
                    logger.info(f"Unit {army2_unit.id} from {army2.name} has attacked unit {army1_unit.id} from {army1.name}")
                    logger.success(f"Unit {army2_unit.id} from {army2.name} has damaged unit {army1_unit.id} from {army1.name}")

                logger.info(f"Health of unit {army1_unit.id} from {army1.name}: {army1_unit.health}")
                logger.info(f"Health of unit {army2_unit.id} from {army2.name}: {army2_unit.health}")

                # Удаление юнита из БД, если он умер (а также вывод информации о падшем бойце)
                if is_first and army2_unit.health <= 0:
                    await GameManager.delete_with_log_unit(army2_unit, army2)
                elif not is_first and army1_unit.health <= 0:
                    await GameManager.delete_with_log_unit(army1_unit, army1)

            # Обновляем списки юнитов для каждой армии
            units1 = await get_army_units(army1.id)
            units2 = await get_army_units(army2.id)
            is_first = not is_first                       # Меняем очередность хода

            # Проверка задержки
            t2 = time.perf_counter()
            t_diff = t2 - t1 
            if t_diff > timeout:
                logger.info(f"Timeout for fight {army1.name} VS {army2.name}")
                # Обновляем списки юнитов для каждой армии
                units1 = await get_army_units(army1.id)
                units2 = await get_army_units(army2.id)
                break
            
        if units1 and not units2:
            # Если остались юниты в 1 армии и не осталось во 2
            army1 = await Army.filter(id=army1.id).first()
            army1.fight_with_id = None
            await army1.save()
            del_army = await Army.filter(id=army2.id).delete()
            logger.info(f"Army {del_army.name} with id {del_army.id} was deleted")
            logger.success(f"Army {army1.name} with id {army1.id} won!")
            return army1
        elif not units1 and units2:
            # Если остались юниты в 2 армии и не осталось во 1
            army2 = await Army.filter(id=army2.id).first()
            army2.fight_with_id = None
            await army2.save()
            del_army = await Army.filter(id=army1.id).delete()
            logger.info(f"Army {del_army.name} with id {del_army.id} was deleted")
            logger.success(f"Army {army2.name} with id {army2.id} won!")
            return army2
        else:
            raise InvalidFightResultException("Недействительный исход боя")


    @classmethod
    async def _play(cls, _game: Game) -> Game:
        # Логика игрового процесса
        # 1. Выгружаем данные об игре из кэша
        game_dict = dict()
        with open('../__game_cache__', 'rb') as file:
            game_dict = pickle.load(file)
            if not game_dict:
                logger.error(f"Нет данных для игры")
                raise ValueError("Нет данных для игры")
            else:
                logger.success("Данные об игре выгружены из кэша")
            
        armies_list = await Army.all().order_by('id')  # Список участвующих в игре армий
        armies: dict[int, Army] = dict()
        for army in armies_list:
            armies[army.id] = army

        army_in_figths: set = set()          # Армии, которые находятся в бою
        id_list = list(armies.keys())   # Список id армий

        ##################################################
        # Отладочная часть
        logger.debug(f"Спиок армий:\n{armies}")


        ##################################################

        logger.info("Point 1")
            
        while len(armies) > 1:
            # Цикл организации сражений
            for id, army in armies.items():
                # Поиск соперника для армии

                if army in army_in_figths:
                    # Если армия была в бою
                    is_exist = await is_exist_army(army.fight_with_id)
                    if not is_exist:    # Проверка сущствования армии-соперника в базе
                        logger.info(f"\n\nУ армии {army.id} {army.name} нет противника")
                        logger.info(f"Информация об армии:\n{army}")
                        army_in_figths.remove(army)                                          # Убираем у армии метку "в бою"
                        logger.info(f"Информация об армии после удаления метки:\n{army}\n")

                id_list = [id for id in armies.keys()]
                try: 
                    army, army_to_fight, army_in_figths = await GameManager.match_rival(id, army, id_list, army_in_figths) # Подбор армии-соперника
                except Exception as e:
                    if isinstance(e, TimeoutError):
                        logger.warning(f"Не удалось подобрать противника для армии {id}. Вышло время ожидания")
                        continue
                finally:
                    armies[id], armies[army.fight_with_id] = army, army_to_fight  # Обновляем данные об армиях
                army_in_figths.add(armies[id])                                      # Помечаем армии, как "в бою"
                army_in_figths.add(armies[army.fight_with_id])
                w_army = await cls._fight_process(army, army_to_fight, game_dict['gmap'], timeout=120)               # БИТВА!

            armies = await Army.all().order_by('id')

        win_army = await Army.all().first()
        if win_army:
            win_units = await get_army_units(win_army.id)
            win_army_stat: ArmyStatBase = ArmyStatBase(id=win_army.id, name=win_army.name, loss=win_army.count-len(win_units))
            _game.win_army = win_army_stat
        _game.is_play = False
        return _game


    @classmethod
    async def init_fight(cls, game: Game):
        """ Инициализация сражения """
        if not game.is_play:
            return game

        # Сохраняем данные об игре в кэш
        with open("../__game_cache__", 'wb') as file:
            pickle.dump(game, file)

        try:
            await access_game(method='post', game=game) # Загружаем данные игры
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных игры: \n{e}")
            return HTTPException(status_code=503, detail="Game cannot be initialized")
            # Здесь должна быть обработка исключения
            # или выбрасывается кастомное исключение (код ошибки)

        logger.info("Запускаем игру...")
        game = await cls._play(game)
        logger.success("Турнир успешно завершен")

        # Сохраняем данные об игре в кэш
        with open("../__game_cache__", 'wb') as file:
            pickle.dump(game, file)
        return game