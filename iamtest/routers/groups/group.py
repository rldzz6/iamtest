from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from iamtest.commons import util 
import iamtest.models.querys.group as sql
import iamtest.models.requests.group as RequestDTO
import iamtest.models.requests.permission as Permission
from iamtest.models.entity.common import response as Response

router = APIRouter()

#권한그룹 목록 조회
@router.get('/', response_model=Response)
@router.get('/{group_id}', response_model=Response)
def select_group(group_id: str | None = None, model: RequestDTO.Group = Depends()):
    try:
        model.group_id = group_id
        result_data = sql.select_group(model)

        response = Response()
        response.data=[dict(data) for data in result_data]
        return response
    except Exception as error:
        response = Response()
        response.code= error.args[0]
        response.message= error.args[1]
        
        raise HTTPException(status_code=404, detail=response.dict())

#사용자 조회
@router.get('/{group_id}/user', response_model=Response)
def select_group_user(group_id: str):
    try:
        result_data = sql.select_group_user(group_id)

        response = Response()
        response.data=[data.dict(exclude_unset=True, exclude_none=True) for data in result_data]
        return response
    except Exception as error:
        response = Response(code='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#권한 목록
@router.get('/{group_id}/permission', response_model=Response)
def select_group_permission(group_id: str, model: Permission.Permission = Depends()):
    try:
        result_data = sql.select_group_permission(group_id, model)

        response = Response()
        response.data=[dict(data) for data in result_data]
        return response
    except Exception as error:
        response = Response(code='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#권한그룹 생성
@router.post('/', response_model=Response)
async def insert_group(model: RequestDTO.Group):
    try:
        if not util.is_value('group_name', model):
            raise Exception('그룹명을 입력하세요.')
        
        result_data = sql.insert_group(model)

        if not result_data.group_id :
            raise Exception('권한그룹을 생성하는데 실패했습니다.')

        response = Response()
        response.data=[{"group_id":result_data.group_id}]

        return response
    except Exception as error:
        response = Response(code='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#권한그룹 정보 수정
@router.patch('/{group_id}', response_model=Response)
async def update_service(group_id:str, model: RequestDTO.Group):
    try:
        if not group_id:
            raise Exception('권한그룹을 찾을 수 없습니다.')
        if not util.is_value('group_name', model):
            raise Exception('그룹명을 입력하세요.')
    
        result_data = sql.update_group(group_id, model)

        response = Response()
        response.data=[{"group_id" : group_id}]
        return response
    except Exception as error:
        response = Response(code='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#권한그룹 삭제
@router.delete('/{group_id}', response_model=Response)
async def delete_group(group_id:str):
    try:
        if not group_id:
            raise Exception('권한그룸을 찾을 수 없습니다.')
    
        result_data = sql.delete_group(group_id)

        if result_data == 0:
            raise Exception('권한그룹을 삭제하는데 실패했습니다.')

        response = Response()
        return response
    except Exception as error:
        response = Response(code='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())