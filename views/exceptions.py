class UndefinedUnitTypeException(Exception):
    error_code = "UNDEFINED_UNIT_TYPE"

class InvalidFightResultException(Exception):
    error_code = "INVALID_FIGHT_RESULT"

class GameInitializeException(Exception):
    error_code = "GAME_IS_NOT_INITIALIZED"