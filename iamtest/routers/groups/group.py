from fastapi import APIRouter, HTTPException, Depends, Header, Request
from fastapi.responses import JSONResponse
from iamtest.commons import util
import iamtest.models.querys.group as sql
import iamtest.models.querys.permission as permission_sql
import iamtest.models.requests.group as RequestDTO
from iamtest.models.entity.common import Response

router = APIRouter()
category = '권한그룹 관리'

#권한그룹 정보 조회
@router.get('')
@router.get('/{group_id}')
def select_group(request:Request, page: int = 0, model: RequestDTO.Group = Depends()):
    identity = request.headers.get("identity")
    try:
        result_data = sql.select_group(model, page)
        total_count = sql.select_group_count(model)

        response = util.make_response(result_data, total_count)   
        util.log(category, '권한그룹 정보 조회', model, identity)
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#권한그룹 생성
@router.post('')
async def insert_group(request:Request, model: RequestDTO.Group):
    identity = request.headers.get("identity")
    try:
        if not util.is_value('group_name', model) or util.is_empty('group_name', model):
            raise Exception('그룹명을 입력하세요.')
        
        result_data = sql.insert_group(model)

        if not result_data.group_id :
            raise Exception('권한그룹을 생성하는데 실패했습니다.')
 
        response = Response(data={"group_id":result_data.group_id}, total_count=1)
        util.log(category, '권한그룹 생성', model, identity)

        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#권한그룹 정보 수정
@router.patch('/{group_id}')
async def update_service(request:Request, group_id:str, model: RequestDTO.Group):
    identity = request.headers.get("identity")
    try:
        if not group_id:
            raise Exception('권한그룹을 찾을 수 없습니다.')
        if util.is_empty('group_name', model):
            raise Exception('그룹명을 입력하세요.')

        result_count = sql.update_group(group_id, model)

        util.log(category, '권한그룹 정보 수정', model, identity)

        response = Response(data={"group_id" : group_id}, total_count=int(result_count))
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#권한그룹 삭제
@router.delete('/{group_id}')
async def delete_group(request:Request, group_id:str):
    identity = request.headers.get("identity")
    try:
        model = RequestDTO.Group(group_id=group_id)
        if not group_id:
            raise Exception('권한그룹을 찾을 수 없습니다.')
    
        result_count = sql.delete_group(group_id)

        if result_count == 0:
            raise Exception('권한그룹을 삭제하는데 실패했습니다.')

        util.log(category, '권한그룹 삭제', model, identity)
        response = Response(total_count=int(result_count))
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#권한그룹 허용 사원 목록
@router.get('/user/{group_id}')
def select_group_user(request:Request, group_id: str):
    identity = request.headers.get("identity")
    try:
        result_data = sql.select_group_user(group_id)

        response = util.make_response(result_data, 1)   
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#권한그룹에 할당된 권한 목록
@router.get('/permission/{group_id}')
def select_group_permission(request:Request, group_id: str, page:int = 0, model: RequestDTO.Permission = Depends()):
    identity = request.headers.get("identity")
    try:
        result_data = sql.select_group_permission(model, page)
        total_count = sql.select_group_permission_count(group_id, model)

        response = util.make_response(result_data, total_count)
        return response
    except Exception as error:
        response = Response(code='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#권한그룹 사원 및 권한 할당
@router.post('/permission')
async def allocate_group_user(request:Request, model: RequestDTO.Allocation):
    identity = request.headers.get("identity")
    try:
        ##### 허용 사원 저장 #####
        renew_user_list = model.employee_list.replace(' ', '').split(',')
        #기존 할당 사원과 비교한다.
        old_group_info = sql.select_group_user(model.group_id)
        old_user_list = [data.employee_id for data in old_group_info]
        
        #사원에게 권한그룹 신규 할당
        for new_user in list(set(renew_user_list) - set(old_user_list)):
            if new_user:
                data = RequestDTO.Permission(employee_id=new_user, group_id=model.group_id)
                permission_sql.allocation_permission(data)
        #사원에게 할당된 권한그룹 제거
        for clear_user in list(set(old_user_list) - set(renew_user_list)):
            if clear_user:
                permission_sql.clear_permission(model.group_id, clear_user)

        ##### 권한 목록 저장#####
        renew_permission_list = model.permission_list.replace(' ', '').split(',')
        #기존에 할당되어있던 권한 목록
        orl_permission_info = sql.select_group_permission(model)
        orl_permission_list = [data.permission_id for data in orl_permission_info]
        
        #권한그룹에 권한 할당
        for new_permission in list(set(renew_permission_list) - set(orl_permission_list)):
            if new_permission:
                data = RequestDTO.Permission(group_id=model.group_id, permission_id=new_permission)
                sql.allocation_permission(data)
        #권한할당된 권한 제거
        for clear_permission in list(set(orl_permission_list) - set(renew_permission_list)):
            if clear_permission:
                sql.clear_permission(model.group_id, clear_permission)

        util.log(category, '권한그룹 허용사원 및 권한 목록 저장', model, identity)
        response = Response(data={"group_id":model.group_id})
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

