from fastapi import APIRouter, HTTPException, Depends, Header, Request
from typing import Dict, Any
from datetime import datetime
import json, logging
from iamtest.commons import util
import iamtest.models.querys.service as sql
import iamtest.models.requests.service as RequestDTO
from iamtest.models.entity.common import Response

router = APIRouter()
category = '서비스 관리'

#서비스 정보 조회
@router.get('')
@router.get('/{service_id}')
def select_service(request:Request, page: int = 0, model: RequestDTO.Service = Depends()):
    identity = request.headers.get("identity") #header의 사번
    try:
        result_data = sql.select_service(model, page)
        total_count = sql.select_service_count(model)
        
        response = util.make_response(result_data, total_count)
        util.log(category, '서비스 정보 조회', model, identity)
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#서비스 생성
@router.post('')
async def insert_service(request:Request, model: RequestDTO.Service):
    identity = request.headers.get("identity") #header의 사번
    try:
        if not util.is_value('service_name', model) or util.is_empty('service_name', model):
            raise Exception('서비스명을 입력하세요.')

        result_data = sql.insert_service(model)

        if not result_data.service_id :
            raise Exception('서비스를 생성하는데 실패했습니다.')

        response = Response(data={"service_id":result_data.service_id}, total_count=1)
        util.log(category, '서비스 생성', model, identity)
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#서비스 정보 업데이트
@router.patch('/{service_id}')
async def update_service(request:Request, service_id:str, model: RequestDTO.Service):
    identity = request.headers.get("identity") #header의 사번
    try:
        if not service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
        if util.is_empty('service_name', model):
            raise Exception('서비스명을 입력하세요.')

        result_count = sql.update_service(service_id, model)
        
        util.log(category, '서비스 정보 수정', model, identity)
        response = Response(data={"service_id" : service_id}, total_count=int(result_count))
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

@router.delete('/{service_id}')
async def delete_service(request:Request, service_id:str):
    identity = request.headers.get("identity") #header의 사번
    try:
        model = RequestDTO.Service(service_id=service_id)
        if not service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
    
        result_count = sql.delete_service(service_id)

        if result_count == 0:
            raise Exception('서비스를 삭제하는데 실패했습니다.')
        
        util.log(category, '서비스 삭제', model, identity)
        response = Response(total_count=int(result_count))
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())
