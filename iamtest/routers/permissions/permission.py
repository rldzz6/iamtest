from fastapi import APIRouter, HTTPException, Depends, Header, Request
import logging
from didimiam.commons import util 
from didimiam.commons import config
import didimiam.models.querys.permission as sql
import didimiam.models.requests.permission as RequestDTO
from didimiam.models.entity.common import Response

router = APIRouter()
category = '권한 관리'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#권한 정보 조회
@router.get('')
@router.get('/{permission_id}')
def select_permission(request:Request, page: int = 0, model: RequestDTO.Permission = Depends()):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        result_data = sql.select_permission(db, model, page)
        total_count = sql.select_permission_count(db, model)

        response = util.make_response(result_data, total_count[0])
        util.log(category, '권한 정보 조회', model, identity)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#권한 사용자 목록 조회
#TODO:권한 또는 권한 그룹의 사용자 조회
@router.get('/user/{employee_id}', response_model=Response)
@router.get('/{permission_id}/users', response_model=Response)
def select_user(request:Request, page: int = 0, model: RequestDTO.Permission = Depends()):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        result_data = sql.select_user(model, page)
        total_count = sql.select_user_count(model)

        response = util.make_response(result_data, total_count[0])
        util.log(category, '권한 정보 조회', model, identity)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#권한 생성
@router.post('')
async def insert_permission(request:Request, model: RequestDTO.Permission):
    identity = request.headers.get("identity")
    db = config.db_connection()
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
        
        result_data = sql.insert_permission(db, model)

        if not result_data :
            raise Exception('권한을 생성하는데 실패했습니다.')

        response = Response(data={"permission_id":result_data}, total_count=1)
        util.log(category, '권한 생성', model, identity)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#권한 정보 업데이트
@router.patch('/{permission_id}')
async def update_service(request:Request, permission_id:str, model: RequestDTO.Permission):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        if not permission_id:
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

        result = sql.update_permission(db, permission_id, model)

        util.log(category, '권한 정보 수정', model, identity)
        response = Response(data={"permission_id" : permission_id})
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#권한 삭제
@router.delete('/{permission_id}')
async def delete_permission(request:Request, permission_id:str):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        model = RequestDTO.Permission(permission_id=permission_id)
        if not permission_id:
            raise Exception('권한을 찾을 수 없습니다.')
    
        result_count = sql.delete_permission(db, permission_id)

        #if result_count == 0:
        #    raise Exception('권한을 삭제하는데 실패했습니다.')

        util.log(category, '권한 삭제', model, identity)
        response = Response()
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()


#사용자 권한 정보 저장
@router.post('/user')
async def allocate_permission(request:Request, model: RequestDTO.Allocation):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        if not util.is_value('employee_id', model) or util.is_empty('employee_id', model):
            raise Exception('사원정보가 올바르지 않습니다.')

        #사원의 기존 권한 목록
        old_user_permission = sql.select_user(model)
        old_permission_list = [str(data.permission_id) for data in old_user_permission]
        old_group_list = [str(data.group_id) for data in old_user_permission]

        #신규로 할당할 권한과 삭제할 권한 모델을 리스트에 저장한다.
        permission_alloctation_list = []
        permission_clear_list = []

        #권한 할당
        for new_permission in list(set(model.permission_list) - set(old_permission_list)):
            if new_permission:
                permission_alloctation_list.append(RequestDTO.User(employee_id=model.employee_id, permission_id=new_permission))
        #권한그룹 할당
        for new_group in list(set(model.group_list) - set(old_group_list)):
            if new_group:
                permission_alloctation_list.append(RequestDTO.User(employee_id=model.employee_id, group_id=new_group))

        #권한 삭제
        for clear_permission in list(set(old_permission_list) - set(model.permission_list)):
            if clear_permission:
                permission_clear_list.append(RequestDTO.User(employee_id=model.employee_id, permission_id=clear_permission))
        #권한그룹 삭제
        for clear_group in list(set(old_group_list) - set(model.group_list)):
            if clear_group:
                permission_clear_list.append(RequestDTO.User(employee_id=model.employee_id, group_id=clear_group))

        if len(permission_alloctation_list) > 0:
            allocation_count = sql.allocation_user_permission(db, permission_alloctation_list)
        if len(permission_clear_list) > 0:
            clear_count = sql.clear_user_permission(db, permission_clear_list)

        response = Response(data={"employee_id":model.employee_id})
        util.log(category, '사원 권한 저장', model, identity)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()
