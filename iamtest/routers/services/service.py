from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import json
from iamtest.commons import util 
import iamtest.models.querys.service as sql
import iamtest.models.requests.service as RequestDTO
from iamtest.models.entity.common import response as Response

router = APIRouter()

#서비스 목록 조회
@router.get('/', response_model=Response)
@router.get('/{service_id}', response_model=Response)
def select_service(service_id: str | None = None, model: RequestDTO.Service = Depends()):
    try:
        model.service_id = service_id
        result_data = sql.select_service(model)
        
        response = Response()
        response.data=[dict(data) for data in result_data]
        
        return Response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#서비스 생성
@router.post('/', response_model=Response)
async def insert_service(model: RequestDTO.Service):
    try:
        if not util.is_value('service_name', model):
            raise Exception('서비스명을 입력하세요.')

        result_data = sql.insert_service(model)

        if result_data.service_id :
            raise Exception('서비스를 생성하는데 실패했습니다.')

        response = Response()
        response.data=[{"service_id":result_data.service_id}]

        return response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

@router.patch('/{service_id}', response_model=Response)
async def update_service(service_id:str, model: RequestDTO.Service):
    try:
        if not service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
        if not util.is_value('service_name', model):
            raise Exception('서비스명을 입력하세요.')
    
        result_data = sql.update_service(service_id, model)

        response = Response()
        response.data=[{"service_id" : service_id}]
        return response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

@router.delete('/{service_id}', response_model=Response)
async def delete_service(service_id:str):
    try:
        if not service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
    
        result_data = sql.delete_service(service_id)

        if result_data == 0:
            raise Exception('서비스를 삭제하는데 실패했습니다.')
        
        response = Response()
        return response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())