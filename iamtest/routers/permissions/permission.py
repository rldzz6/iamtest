from fastapi import APIRouter, HTTPException, Depends, Header, Request
from iamtest.commons import util 
import iamtest.models.querys.permission as sql
import iamtest.models.requests.permission as RequestDTO
from iamtest.models.entity.common import Response

router = APIRouter()
category = '권한'

#권한 정보 조회
@router.get('')
@router.get('/{permission_id}')
def select_permission(request:Request, page: int = 0, model: RequestDTO.Permission = Depends()):
    identity = request.headers.get("identity")
    try:
        result_data = sql.select_permission(model, page)
        total_count = sql.select_permission_count(model)

        response = util.make_response(result_data, total_count)
        util.log(category, '권한 정보 조회', model, identity)
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#권한 사용자 목록 조회
#TODO:권한 또는 권한 그룹의 사용자 조회
@router.get('/user/{employee_id}', response_model=Response)
@router.get('/{permission_id}/users', response_model=Response)
def select_user(permission_id: str | None = None, employee_id: str | None = None, model: RequestDTO.Permission = Depends()):
    try:
        model.permission_id = permission_id
        model.employee_id = employee_id
        result_data = sql.select_user(model)

        response = Response()
        response.data=[dict(data) for data in result_data]
        return response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#권한 생성
@router.post('')
async def insert_permission(request:Request, model: RequestDTO.Permission):
    identity = request.headers.get("identity")
    try:
        if not util.is_value('service_id', model) or util.is_empty('service_id', model):
            raise Exception('서비스 정보가 없습니다.')
        if not util.is_value('resource_id', model) or util.is_empty('resource_id', model):
            raise Exception('리소스 정보가 없습니다.')
        if not util.is_value('permission_name', model) or util.is_empty('permission_name', model):
            raise Exception('권한명을 입력하세요.')
        if not util.is_value('permission', model) or util.is_empty('permission', model):
            raise Exception('권한을 선택하세요.')
        if model.permission == '0':
            raise Exception('권한을 선택하세요')
        
        result_data = sql.insert_permission(model)

        if not result_data.permission_id :
            raise Exception('권한을 생성하는데 실패했습니다.')

        response = Response(data={"permission_id":result_data.permission_id}, total_count=1)
        util.log(category, '권한 생성', model, identity)
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#권한 정보 업데이트
@router.patch('/{permission_id}')
async def update_service(request:Request,  permission_id:str, model: RequestDTO.Permission):
    identity = request.headers.get("identity")
    try:
        if permission_id:
            raise Exception('권한 정보를 찾을 수 없습니다.')
        if util.is_empty('service_id', model):
            raise Exception('서비스 정보가 없습니다.')
        if util.is_empty('resource_id', model):
            raise Exception('리소스 정보가 없습니다.')
        if util.is_empty('permission_name', model):
            raise Exception('권한명을 입력하세요.')
        if util.is_empty('permission', model):
            raise Exception('권한을 선택하세요.')
        if model.permission == '0':
            raise Exception('권한을 선택하세요')

        result_count = sql.update_permission(permission_id, model)

        util.log(category, '권한 정보 수정', model, identity)
        response = Response(data={"permission_id" : permission_id}, total_count=int(result_count))
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#권한 삭제
@router.delete('/{permission_id}')
async def delete_permission(request:Request, permission_id:str):
    identity = request.headers.get("identity")
    try:
        model = RequestDTO.Permission(permission_id=permission_id)
        if not permission_id:
            raise Exception('권한을 찾을 수 없습니다.')
    
        result_count = sql.delete_permission(permission_id)

        if result_count == 0:
            raise Exception('권한을 삭제하는데 실패했습니다.')

        util.log(category, '권한 삭제', model, identity)
        response = Response(total_count=int(result_count))
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())
