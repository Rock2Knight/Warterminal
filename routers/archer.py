from fastapi import APIRouter, Response, status, HTTPException
from access.archer import access_archer
from dto.archer_dto import ArcherDto

archer_router = APIRouter(prefix="/archer", tags=["Лучники"])

@archer_router.get("/{id}")
async def get_archer(id: int, response: Response):

    archer_model = {'method': 'get', 'id': id}
    archer_resp = await access_archer(**archer_model)
    
    if isinstance(archer_resp, dict):
        return archer_resp
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return archer_resp     # Если возникла ошибка


@archer_router.post("/{id}/{army_id}")
async def create_archer(id: int, army_id: int, archer_dto: ArcherDto.Create, response: Response):

    archer_model = {'method': 'post', 'army_id': army_id, 'dto': archer_dto}
    archer_resp = await access_archer(**archer_model)
    response.status_code = status.HTTP_201_CREATED
    return archer_resp

@archer_router.put("/{id}/{army_id}")
async def put_archer(id: int, army_id: int, archer_dto: ArcherDto.Update, response: Response):

    archer_model = {'method': 'put', 'army_id': army_id, 'dto': archer_dto}
    archer_resp = await access_archer(**archer_model)
    if isinstance(archer_resp, dict):
        response.status_code = status.HTTP_201_CREATED
        return archer_resp
    elif isinstance(archer_resp, HTTPException):
        response.status_code = archer_resp.status_code
        return HTTPException(status_code=archer_resp.status_code)     


@archer_router.patch("/{id}/{army_id}")
async def patch_archer(id: int, army_id: int, archer_dto: ArcherDto.Update, response: Response):

    archer_model = {'method': 'patch', 'army_id': army_id, 'dto': archer_dto}
    archer_resp = await access_archer(**archer_model)
    if isinstance(archer_resp, HTTPException):
        response.status_code = archer_resp.status_code
        return HTTPException(status_code=archer_resp.status_code)
    response.status_code = status.HTTP_201_CREATED
    return archer_resp
    

@archer_router.delete("/{id}")
async def delete_archer(id: int, response: Response):

    archer_model = {'method': 'delete', 'id': id}
    archer_resp = await access_archer(**archer_model)
    if isinstance(archer_resp, HTTPException):
        response.status_code = archer_resp.status_code
    return archer_resp     # Если возникла ошибка