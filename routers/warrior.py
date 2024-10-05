from fastapi import APIRouter, Response, status
from access.warrior import access_warrior
from dto.warrior_dto import WarriorDto

warrior_router = APIRouter(prefix="/warrior", tags=["Воины"])


@warrior_router.get("/{id}")
async def get_warrior(id: int, response: Response):

    warrior_model = {'method': 'get', 'id': id}
    warrior_resp = await access_warrior(**warrior_model)
    
    if isinstance(warrior_resp, dict):
        return warrior_resp
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return warrior_resp     # Если возникла ошибка


@warrior_router.post("/{id}/{army_id}")
async def create_warrior(id: int, army_id: int, warrior_dto: WarriorDto.Create, response: Response):

    warrior_model = {'method': 'post', 'army_id': army_id, 'dto': warrior_dto}
    warrior_resp = await access_warrior(**warrior_model)
    response.status_code = status.HTTP_201_CREATED
    return warrior_resp


@warrior_router.put("/{id}/{army_id}")
async def put_warrior(id: int, army_id: int, warrior_dto: WarriorDto.Update, response: Response):

    warrior_model = {'method': 'put', 'army_id': army_id, 'dto': warrior_dto}
    warrior_resp = await access_warrior(**warrior_model)
    if isinstance(warrior_resp, dict):
        response.status_code = status.HTTP_201_CREATED
        return warrior_resp
    elif isinstance(warrior_resp, HTTPException):
        response.status_code = warrior_resp.status_code
        return warrior_resp     


@warrior_router.patch("/{id}/{army_id}")
async def patch_warrior(id: int, army_id: int, warrior_dto: WarriorDto.Update, response: Response):

    warrior_model = {'method': 'patch', 'army_id': army_id, 'dto': warrior_dto}
    warrior_resp = await access_warrior(**warrior_model)
    if isinstance(warrior_resp, HTTPException):
        response.status_code = warrior_resp.status_code
    else:
        response.status_code = status.HTTP_201_CREATED
    return warrior_resp

@warrior_router.delete("/{id}")
async def delete_warrior(id: int, response: Response):

    warrior_model = {'method': 'delete', 'id': id}
    warrior_resp = await access_warrior(**warrior_model)
    if isinstance(warrior_resp, HTTPException):
        response.status_code = warrior_resp.status_code
    return warrior_resp     # Если возникла ошибка