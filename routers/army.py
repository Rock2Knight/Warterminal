from fastapi import APIRouter, Response, status, HTTPException
from access.army import access_army
from dto.army_dto import ArmyDto

army_router = APIRouter(prefix="/army", tags=["Армии"])

@army_router.get("/{id}")
async def get_army(id: int, response: Response):

    army_model = {'method': 'get', 'id': id}
    army_resp = await access_army(**army_model)
    if isinstance(army_resp, dict):
        return army_resp
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return army_resp     # Если возникла ошибка


@army_router.post("/{id}/{name}/{count}")
async def create_army(id: int, name: str, count: int, army_dto: ArmyDto.Create, response: Response):
    
    army_model = {'method': 'post', 'army_id': army_dto.id, 'army_dto': army_dto}
    army_resp = await access_army(**army_model)
    return army_resp


@army_router.put("/{id}")
async def put_army(id: int, army_dto: ArmyDto.Update, response: Response):

    army_model = {'method': 'put', 'army_id': army_dto.id, 'army_dto': army_dto}
    army_resp = await access_army(**army_model)
    if isinstance(army_resp, dict):
        response.status_code = status.HTTP_201_CREATED
        return army_resp
    elif isinstance(army_resp, HTTPException):
        response.status_code = army_resp.status_code
        return army_resp     


@army_router.patch("/{id}")
async def patch_army(id: int, army_dto: ArmyDto.Update, response: Response):
    army_model = {'method': 'patch', 'army_id': army_dto.id, 'army_dto': army_dto}
    army_resp = await access_army(**army_model)
    if isinstance(army_resp, HTTPException):
        response.status_code = army_resp.status_code
        return army_resp     
    response.status_code = status.HTTP_201_CREATED
    return army_resp


@army_router.delete("/{id}")
async def delete_army(id: int, response: Response):

    army_model = {'method': 'delete', 'id': id}
    army_resp = await access_army(**army_model)
    if isinstance(army_resp, HTTPException):
        response.status_code = army_resp.status_code
    return army_resp     # Если возникла ошибка