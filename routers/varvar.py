from fastapi import APIRouter, Response, status, HTTPException
from access.varvar import access_varvar
from dto.varvar_dto import VarvarDto

varvar_router = APIRouter(prefix="/varvar", tags=["Варвары"])

@varvar_router.get("/{id}")
async def get_varvar(id: int, response: Response):

    varvar_model = {'method': 'get', 'id': id}
    varvar_resp = await access_varvar(**varvar_model)
    
    if isinstance(varvar_resp, dict):
        return varvar_resp
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return varvar_resp     # Если возникла ошибка


@varvar_router.post("/{id}/{army_id}")
async def create_varvar(id: int, army_id: int, varvar_dto: VarvarDto.Create, response: Response):

    varvar_model = {'method': 'post', 'army_id': army_id, 'dto': varvar_dto}
    varvar_resp = await access_varvar(**varvar_model)
    response.status_code = status.HTTP_201_CREATED
    return varvar_resp

@varvar_router.put("/{id}/{army_id}")
async def put_varvar(id: int, army_id: int, varvar_dto: VarvarDto.Update, response: Response):

    varvar_model = {'method': 'put', 'army_id': army_id, 'dto': varvar_dto}
    varvar_resp = await access_varvar(**varvar_model)
    if isinstance(varvar_resp, dict):
        response.status_code = status.HTTP_201_CREATED
        return varvar_resp
    elif isinstance(varvar_resp, HTTPException):
        response.status_code = varvar_resp.status_code
        return HTTPException(status_code=varvar_resp.status_code)

@varvar_router.patch("/{id}/{army_id}")
async def patch_varvar(id: int, army_id: int, varvar_dto: VarvarDto.Update, response: Response):

    varvar_model = {'method': 'patch', 'army_id': army_id, 'dto': varvar_dto}
    varvar_resp = await access_varvar(**varvar_model)
    if isinstance(varvar_resp, HTTPException):
        response.status_code = varvar_resp.status_code
        return HTTPException(status_code=varvar_resp.status_code)
    response.status_code = status.HTTP_201_CREATED
    return varvar_resp


@varvar_router.delete("/{id}")
async def delete_varvar(id: int, response: Response):

    varvar_model = {'method': 'delete', 'id': id}
    varvar_resp = await access_varvar(**varvar_model)
    if isinstance(varvar_resp, HTTPException):
        response.status_code = varvar_resp.status_code
    return varvar_resp     # Если возникла ошибка