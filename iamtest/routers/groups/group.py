from fastapi import APIRouter, HTTPException, Depends, Header, Request
import logging
from iamtest.commons import util
from iamtest.commons import config
import iamtest.models.querys.group as sql
import iamtest.models.querys.permission as permission_sql
import iamtest.models.requests.group as RequestDTO
from iamtest.models.entity.common import Response

router = APIRouter()
logmodel = RequestDTO.Log()
category = '권한그룹 관리'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#권한그룹 정보 조회
@router.get('')
@router.get('/{group_id}')
def select_group(request:Request, model: RequestDTO.Group = Depends(), page: int = 0):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        result_data = sql.select_group(db, model, page)
        total_count = sql.select_group_count(db, model)

        response = util.make_response(result_data, total_count)   
        util.log(category, '권한그룹 정보 조회',util.log_description(model, logmodel.dict()), identity)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())

#권한그룹 생성
@router.post('')
async def insert_group(request:Request, model: RequestDTO.Group):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        if not util.is_value('group_name', model) or util.is_empty('group_name', model):
            raise Exception('그룹명을 입력하세요.')
        
        result_data = sql.insert_group(db, model)

        if not result_data :
            raise Exception('권한그룹을 생성하는데 실패했습니다.')

        util.log(category, '권한그룹 생성', util.log_description(model, logmodel.dict()), identity)
        response = Response(data={"group_id":result_data}, total_count=1)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#권한그룹 정보 수정
@router.patch('/{group_id}')
async def update_service(request:Request, group_id:str, model: RequestDTO.Group):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        if not group_id:
            raise Exception('권한그룹을 찾을 수 없습니다.')
        if util.is_empty('group_name', model):
            raise Exception('그룹명을 입력하세요.')

        result_count = sql.update_group(db, group_id, model)

        util.log(category, '권한그룹 정보 수정', util.log_description(model, logmodel.dict()), identity)
        response = Response(data={"group_id" : group_id}, total_count=result_count)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#권한그룹 삭제
@router.delete('/{group_id}')
async def delete_group(request:Request, group_id:str):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        model = RequestDTO.Group(group_id=group_id)
        if not group_id:
            raise Exception('권한그룹을 찾을 수 없습니다.')
    
        result_count = sql.delete_group(db, group_id)

        if result_count == 0:
            raise Exception('권한그룹을 삭제하는데 실패했습니다.')

        util.log(category, '권한그룹 삭제', util.log_description(model, logmodel.dict()), identity)
        response = Response()
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#권한그룹 허용 사원 목록
@router.get('/{group_id}/user')
def select_group_user(request:Request, group_id: str):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        result_data = sql.select_group_user(db, group_id)

        response = util.make_response(result_data, 1)   
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#권한그룹에 할당된 권한 목록
@router.get('/{group_id}/permission')
def select_group_permission(request:Request, group_id: str, page:int = 0, model: RequestDTO.Permission = Depends()):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        result_data = sql.select_group_permission(db, model, page)
        total_count = sql.select_group_permission_count(db, group_id, model)

        response = util.make_response(result_data, total_count)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#권한그룹 사원 및 권한 할당
@router.post('/permission')
async def allocate_group_user(request:Request, model: RequestDTO.Allocation):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        if not util.is_value('group_id', model) or util.is_empty('group_id', model):
            raise Exception('그룹정보가 올바르지 않습니다.')
        ##### 허용 사원 저장 #####
        #기존 할당 사원과 비교한다.
        old_group_info = sql.select_group_user(db, model.group_id)
        old_user_list = [str(data.employee_id) for data in old_group_info]

        #사원에게 할당/할당해제할 권한을 리스트에 저장한다.
        user_allocation_list = []
        user_clear_list = []

        #사원에게 권한그룹 신규 할당
        for new_user in list(set(model.employee_list) - set(old_user_list)):
            if new_user:
                user_allocation_list.append((new_user, None, model.group_id))
        #사원에게 할당된 권한그룹 제거
        for clear_user in list(set(old_user_list) - set(model.employee_list)):
            if clear_user:
                user_clear_list.append((clear_user, None, model.group_id))

        if len(user_allocation_list) > 0:
            permission_sql.allocation_user_permission(db, user_allocation_list)
        if len(user_clear_list) > 0:
            permission_sql.clear_user_permission(db, user_clear_list)

        ##### 권한 목록 저장#####
        #기존에 할당되어있던 권한 목록
        orl_permission_info = sql.select_group_permission(db, model)
        orl_permission_list = [data.permission_id for data in orl_permission_info]
 
        #권한그룹에 할당/할당해제할 권한을 리스트에 저장한다.
        permission_allocation_list = []
        permission_clear_list = []

        #권한그룹에 권한 할당
        print(model.permission_list)
        for new_permission in list(set(model.permission_list) - set(orl_permission_list)):
            if new_permission:
                permission_allocation_list.append((model.group_id, new_permission))
        #권한할당된 권한 제거
        for clear_permission in list(set(orl_permission_list) - set(model.permission_list)):
            if clear_permission:
                permission_clear_list.append((model.group_id, clear_permission))

        if len(permission_allocation_list) > 0:
            sql.allocation_group_permission(db, permission_allocation_list)
        if len(permission_clear_list) > 0:
            sql.clear_group_permission(db, permission_clear_list)     

        util.log(category, '권한그룹 허용사원 및 권한 목록 저장', util.log_description(model, logmodel.dict()), identity)
        response = Response(data={"group_id":model.group_id})
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()