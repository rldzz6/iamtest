from fastapi import APIRouter, HTTPException, Depends, Header, Request
from typing import Dict, Any
import json
from iamtest.commons import util 
import iamtest.models.querys.service as sql
import iamtest.models.requests.service as RequestDTO
from iamtest.models.entity.common import response as Response

router = APIRouter()
log_category = '서비스 관리'
log_work_type = ''
log_description = ''

#서비스 목록 조회
@router.get('/', response_model=Response)
@router.get('/{service_id}', response_model=Response)
def select_service(service_id: str | None = None, model: RequestDTO.Service = Depends(), identity: str = Header(default=None)):
    log_work_type = 'GET'
    log_description = '서비스 목록 조회'

    try:
        model.service_id = service_id
        result_data = sql.select_service(model)
        
        util.log(log_category, log_work_type, log_description, model, 1, identity)
        response = Response(data=[dict(data) for data in result_data])
        return response
    except Exception as error:
        util.log(log_category, log_work_type, log_description, model, 9, identity, str(error))
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#서비스 생성
@router.post('/', response_model=Response)
async def insert_service(model: RequestDTO.Service, identity: str = Header(default=None)):
    log_work_type = 'POST'
    log_description = '서비스 생성'

    try:
        if not util.is_value('service_name', model):
            raise Exception('서비스명을 입력하세요.')

        result_data = sql.insert_service(model)

        if result_data.service_id :
            raise Exception('서비스를 생성하는데 실패했습니다.')

        util.log(log_category, log_work_type, log_description, model, 1, identity)
        response = Response(data=[{"service_id":result_data.service_id}])
        return response
    except Exception as error:
        util.log(log_category, log_work_type, log_description, model, 9, identity, str(error))
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

@router.patch('/{service_id}', response_model=Response)
async def update_service(service_id:str, model: RequestDTO.Service, identity: str = Header(default=None)):    
    log_work_type = 'PATCH'
    log_description = '서비스 정보 수정'

    try:
        if not service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
        if not util.is_value('service_name', model):
            raise Exception('서비스명을 입력하세요.')
    
        result_data = sql.update_service(service_id, model)

        util.log(log_category, log_work_type, log_description, model, 1, identity)
        response = Response(data=[{"service_id" : service_id}])
        return response
    except Exception as error:
        util.log(log_category, log_work_type, log_description, model, 9, identity, str(error))
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

@router.delete('/{service_id}', response_model=Response)
async def delete_service(service_id:str, identity: str = Header(default=None)):
    log_work_type = 'DELETE'
    log_description = '서비스 삭제'

    try:
        model = RequestDTO.Service(service_id = service_id)
        if not service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
    
        result_data = sql.delete_service(service_id)

        if result_data == 0:
            raise Exception('서비스를 삭제하는데 실패했습니다.')
        
        util.log(log_category, log_work_type, log_description, model, 1, identity)
        response = Response()
        return response
    except Exception as error:
        util.log(log_category, log_work_type, log_description, model, 9, identity, str(error))
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())