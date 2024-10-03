from imports import *

logger.add("debug_10_02.log", format="{time} | {level}   | {module}:{function}:{line} - {message}", level="DEBUG", backtrace=True)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Подключение и инициализация схем при старте
    register_tortoise(
        app,
        config=DB_CONFIG,
        generate_schemas=False,  # Автоматическое создание схем при старте
        add_exception_handlers=True,  # Добавляем обработчики ошибок для Tortoise
    )

@app.on_event("shutdown")
async def shutdown_event():
    # Закрытие соединений при завершении работы приложения
    await Tortoise.close_connections()


# Для армии

@app.get("/army/{id}")
async def get_army(id: int, response: Response):

    army_model = {'method': 'get', 'id': id}
    army_resp = await access_army(**army_model)
    if isinstance(army_resp, dict):
        return army_resp
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return army_resp     # Если возникла ошибка


@app.post("/army/{id}/{name}/{count}")
async def create_army(id: int, name: str, count: int, army_dto: ArmyDto.Create, response: Response):
    
    army_model = {'method': 'post', 'army_id': army_dto.id, 'army_dto': army_dto}
    army_resp = await access_army(**army_model)
    return army_resp


@app.put("/army/{id}")
async def put_army(id: int, army_dto: ArmyDto.Update, response: Response):

    army_model = {'method': 'put', 'army_id': army_dto.id, 'army_dto': army_dto}
    army_resp = await access_army(**army_model)
    if isinstance(army_resp, dict):
        response.status_code = status.HTTP_201_CREATED
        return army_resp
    elif isinstance(army_resp, HTTPException):
        response.status_code = army_resp.status_code
        return army_resp     


@app.patch("/army/{id}")
async def patch_army(id: int, army_dto: ArmyDto.Update, response: Response):
    army_model = {'method': 'patch', 'army_id': army_dto.id, 'army_dto': army_dto}
    army_resp = await access_army(**army_model)
    if isinstance(army_resp, HTTPException):
        response.status_code = army_resp.status_code
        return army_resp     
    response.status_code = status.HTTP_201_CREATED
    return army_resp


@app.delete("/army/{id}")
async def delete_army(id: int, response: Response):

    army_model = {'method': 'delete', 'id': id}
    army_resp = await access_army(**army_model)
    if isinstance(army_resp, HTTPException):
        response.status_code = army_resp.status_code
    return army_resp     # Если возникла ошибка


# Для воина

@app.get("/warrior/{id}")
async def get_warrior(id: int, response: Response):

    warrior_model = {'method': 'get', 'id': id}
    warrior_resp = await access_warrior(**warrior_model)
    
    if isinstance(warrior_resp, dict):
        return warrior_resp
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return warrior_resp     # Если возникла ошибка


@app.post("/warrior/{id}/{army_id}")
async def create_warrior(id: int, army_id: int, warrior_dto: WarriorDto.Create, response: Response):

    warrior_model = {'method': 'post', 'army_id': army_id, 'dto': warrior_dto}
    warrior_resp = await access_warrior(**warrior_model)
    response.status_code = status.HTTP_201_CREATED
    return warrior_resp


@app.put("/warrior/{id}/{army_id}")
async def put_warrior(id: int, army_id: int, warrior_dto: WarriorDto.Update, response: Response):

    warrior_model = {'method': 'put', 'army_id': army_id, 'dto': warrior_dto}
    warrior_resp = await access_warrior(**warrior_model)
    if isinstance(warrior_resp, dict):
        response.status_code = status.HTTP_201_CREATED
        return warrior_resp
    elif isinstance(warrior_resp, HTTPException):
        response.status_code = warrior_resp.status_code
        return warrior_resp     


@app.patch("/warrior/{id}/{army_id}")
async def patch_warrior(id: int, army_id: int, warrior_dto: WarriorDto.Update, response: Response):

    warrior_model = {'method': 'patch', 'army_id': army_id, 'dto': warrior_dto}
    warrior_resp = await access_warrior(**warrior_model)
    if isinstance(warrior_resp, HTTPException):
        response.status_code = warrior_resp.status_code
    else:
        response.status_code = status.HTTP_201_CREATED
    return warrior_resp

@app.delete("/warrior/{id}")
async def delete_warrior(id: int, response: Response):

    warrior_model = {'method': 'delete', 'id': id}
    warrior_resp = await access_warrior(**warrior_model)
    if isinstance(warrior_resp, HTTPException):
        response.status_code = warrior_resp.status_code
    return warrior_resp     # Если возникла ошибка


# Для лучника


@app.get("/archer/{id}")
async def get_archer(id: int, response: Response):

    archer_model = {'method': 'get', 'id': id}
    archer_resp = await access_archer(**archer_model)
    
    if isinstance(archer_resp, dict):
        return archer_resp
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return archer_resp     # Если возникла ошибка


@app.post("/archer/{id}/{army_id}")
async def create_archer(id: int, army_id: int, archer_dto: ArcherDto.Create, response: Response):

    archer_model = {'method': 'post', 'army_id': army_id, 'dto': archer_dto}
    archer_resp = await access_archer(**archer_model)
    response.status_code = status.HTTP_201_CREATED
    return archer_resp

@app.put("/archer/{id}/{army_id}")
async def put_archer(id: int, army_id: int, archer_dto: ArcherDto.Update, response: Response):

    archer_model = {'method': 'put', 'army_id': army_id, 'dto': archer_dto}
    archer_resp = await access_archer(**archer_model)
    if isinstance(archer_resp, dict):
        response.status_code = status.HTTP_201_CREATED
        return archer_resp
    elif isinstance(archer_resp, HTTPException):
        response.status_code = archer_resp.status_code
        return HTTPException(status_code=archer_resp.status_code)     


@app.patch("/archer/{id}/{army_id}")
async def patch_archer(id: int, army_id: int, archer_dto: ArcherDto.Update, response: Response):

    archer_model = {'method': 'patch', 'army_id': army_id, 'dto': archer_dto}
    archer_resp = await access_archer(**archer_model)
    if isinstance(archer_resp, HTTPException):
        response.status_code = archer_resp.status_code
        return HTTPException(status_code=archer_resp.status_code)
    response.status_code = status.HTTP_201_CREATED
    return archer_resp
    

@app.delete("/archer/{id}")
async def delete_archer(id: int, response: Response):

    archer_model = {'method': 'delete', 'id': id}
    archer_resp = await access_archer(**archer_model)
    if isinstance(archer_resp, HTTPException):
        response.status_code = archer_resp.status_code
    return archer_resp     # Если возникла ошибка

# Для варвара

@app.get("/varvar/{id}")
async def get_varvar(id: int, response: Response):

    varvar_model = {'method': 'get', 'id': id}
    varvar_resp = await access_varvar(**varvar_model)
    
    if isinstance(varvar_resp, dict):
        return varvar_resp
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return varvar_resp     # Если возникла ошибка


@app.post("/varvar/{id}/{army_id}")
async def create_varvar(id: int, army_id: int, varvar_dto: VarvarDto.Create, response: Response):

    varvar_model = {'method': 'post', 'army_id': army_id, 'dto': varvar_dto}
    varvar_resp = await access_varvar(**varvar_model)
    response.status_code = status.HTTP_201_CREATED
    return varvar_resp

@app.put("/varvar/{id}/{army_id}")
async def put_varvar(id: int, army_id: int, varvar_dto: VarvarDto.Update, response: Response):

    varvar_model = {'method': 'put', 'army_id': army_id, 'dto': varvar_dto}
    varvar_resp = await access_varvar(**varvar_model)
    if isinstance(varvar_resp, dict):
        response.status_code = status.HTTP_201_CREATED
        return varvar_resp
    elif isinstance(varvar_resp, HTTPException):
        response.status_code = varvar_resp.status_code
        return HTTPException(status_code=varvar_resp.status_code)

@app.patch("/varvar/{id}/{army_id}")
async def patch_varvar(id: int, army_id: int, varvar_dto: VarvarDto.Update, response: Response):

    varvar_model = {'method': 'patch', 'army_id': army_id, 'dto': varvar_dto}
    varvar_resp = await access_varvar(**varvar_model)
    if isinstance(varvar_resp, HTTPException):
        response.status_code = varvar_resp.status_code
        return HTTPException(status_code=varvar_resp.status_code)
    response.status_code = status.HTTP_201_CREATED
    return varvar_resp


@app.delete("/varvar/{id}")
async def delete_varvar(id: int, response: Response):

    varvar_model = {'method': 'delete', 'id': id}
    varvar_resp = await access_varvar(**varvar_model)
    if isinstance(varvar_resp, HTTPException):
        response.status_code = varvar_resp.status_code
    return varvar_resp     # Если возникла ошибка

@app.post("/game/{army_count}/{units_count}")
async def start_game(army_count: int, units_count: int, game: Game, response: Response):

    game_result = await Fight.init_fight(game)  # Запускаем игру
    if not isinstance(game_result, HTTPException):
        response.status_code = status.HTTP_201_CREATED
        return game_result.model_dump()
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return game_result     # Если возникла ошибка