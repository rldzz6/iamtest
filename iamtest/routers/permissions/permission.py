from fastapi import APIRouter, HTTPException, Depends
from iamtest.commons import util 
import iamtest.models.querys.permission as sql
import iamtest.models.requests.permission as RequestDTO
from iamtest.models.entity.common import response as Response

router = APIRouter()

#권한 목록 조회
@router.get('/', response_model=Response)
@router.get('/{permission_id}', response_model=Response)
def select_permission(permission_id: str, model: RequestDTO.Permission = Depends()):
    try:
        result_data = sql.select_permission(model)

        response = Response()
        response.data=[dict(data) for data in result_data]
        return response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#권한 사용자 목록 조회
@router.get('/users', response_model=Response)
@router.get('/{permission_id}/users', response_model=Response)
def select_user(permission_id: str | None = None, model: RequestDTO.Permission = Depends()):
    try:
        model.permission_id = permission_id
        result_data = sql.select_user(model)

        response = Response()
        response.data=[dict(data) for data in result_data]
        return response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#권한 생성
@router.post('/', response_model=Response)
async def insert_permission(model: RequestDTO.Permission):
    try:
        if not util.is_value('service_id', model):
            raise Exception('서비스 정보가 없습니다.')
        if not util.is_value('resource_id', model):
            raise Exception('리소스 정보가 없습니다.')
        if not util.is_value('permission_name', model):
            raise Exception('권한명을 입력하세요.')
        if not util.is_value('permission', model):
            raise Exception('권한을 선택하세요.')
        if model.permission == '0':
            raise Exception('권한을 선택하세요')
        
        result_data = sql.insert_permission(model)

        if not result_data.permission_id :
            raise Exception('권한을 생성하는데 실패했습니다.')
        
        response = Response()
        response.data=[{"permission_id":result_data.permission_id}]

        return response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#권한 정보 업데이트
@router.patch('/{permission_id}', response_model=Response)
async def update_service(permission_id:str, model: RequestDTO.Permission):
    try:
        if not permission_id:
            raise Exception('권한 정보를 찾을 수 없습니다.')
        if not util.is_value('service_id', model):
            raise Exception('서비스 정보가 없습니다.')
        if not util.is_value('resource_id', model):
            raise Exception('리소스 정보가 없습니다.')
        if not util.is_value('permission_name', model):
            raise Exception('권한명을 입력하세요.')
        if not util.is_value('permission', model):
            raise Exception('권한을 선택하세요.')
        if model.permission == '0':
            raise Exception('권한을 선택하세요')

        result_data = sql.update_permission(permission_id, model)

        response = Response()
        response.data=[{"permission_id":permission_id}]
        return response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#권한 삭제
@router.delete('/{permission_id}', response_model=Response)
async def delete_permission(permission_id:str):
    try:
        if not permission_id:
            raise Exception('권한을 찾을 수 없습니다.')
    
        result_data = sql.delete_permission(permission_id)

        if result_data == 0:
            raise Exception('권한을 삭제하는데 실패했습니다.')

        response = Response()
        return response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())
