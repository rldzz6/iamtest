from fastapi import APIRouter, HTTPException, Depends, Header, Request
from typing import Dict, Any
from datetime import datetime
import logging
from iamtest.commons import util 
import iamtest.models.querys.resource as sql
import iamtest.models.requests.resource as RequestDTO
from iamtest.models.entity.common import Response
from iamtest.models.entity.common import Errorlog as Errorlog

router = APIRouter()
category = '리소스 관리'

#리소스 목록 조회
@router.get('')
@router.get('/{resource_id}')
def select_resource(request:Request, page: int = 0, model: RequestDTO.Resource = Depends()):
    identity = request.headers.get("identity") #header의 사번
    try:
        result_data = sql.select_resource(model, page)
        total_count = sql.select_resource_count(model)
        
        response = util.make_response(result_data, total_count)
        util.log(category, '리소스 정보 조회', model, identity)
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#리소스 생성
@router.post('')
async def insert_resource(request:Request, model: RequestDTO.Resource):
    identity = request.headers.get("identity") #header의 사번
    try:
        print(model)
        if not util.is_value('service_id', model) or util.is_empty('service_id', model):
            raise Exception('서비스 정보가 없습니다.')
        if not util.is_value('resource_name', model) or util.is_empty('resource_name', model):
            raise Exception('리소스명을 입력하세요.')
        
        result_data = sql.insert_resource(model)

        if not result_data.resource_id :
            raise Exception('리소스를 생성하는데 실패했습니다.')

        util.log(category, '리소스 생성', model, identity)
        response = Response(data={"resource_id":result_data.resource_id}, total_count=1)
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#리소스 정보 업데이트
@router.patch('/{resource_id}')
async def update_service(request:Request, resource_id:str, model: RequestDTO.Resource):
    identity = request.headers.get("identity") #header의 사번
    try:
        if not resource_id:
            raise Exception('리소스를 찾을 수 없습니다.')
        if util.is_empty('resource_name', model):
            raise Exception('리소스명을 입력하세요.')
        if util.is_empty('service_id', model):
            raise Exception('서비스를 찾을 수 없습니다.')

        result_count = sql.update_resource(resource_id, model)

        util.log(category, '리소스 정보 수정', model, identity)
        response = Response(data={"resource_id" : resource_id}, total_count=int(result_count))
        return response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#f리소스 삭제
@router.delete('/{resource_id}')
async def delete_resource(request:Request, resource_id:str):
    identity = request.headers.get("identity") #header의 사번
    try:
        model = RequestDTO.Resource(resource_id=resource_id)
        if not resource_id:
            raise Exception('리소스를 찾을 수 없습니다.')
    
        result_count = sql.delete_resource(resource_id)

        if result_count == 0:
            raise Exception('리소스를 삭제하는데 실패했습니다.')

        response = Response(total_count=int(result_count))
        util.log(category, '리소스 삭제', model, identity)
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())
