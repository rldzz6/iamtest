from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import json
from iamtest.models.entity.response import response as Response
from iamtest.commons import util 
import iamtest.models.requests.resource as RequestDTO
import iamtest.models.querys.resource as sql

router = APIRouter()

#리소스 목록 조회
@router.get('/', response_model=Response)
@router.get('/{resource_id}', response_model=Response)
def select_resource(resource_id: str | None = None, model: RequestDTO.Resource = Depends()):
    try:
        model.resource_id = resource_id
        result_data = sql.select_resource(model)

        Response.message=''
        Response.data=[dict(data) for data in result_data]
        return Response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#리소스 생성
@router.post('/', response_model=Response)
async def insert_resource(model: RequestDTO.Resource):
    try:
        if not util.is_value('service_id', model):
            raise Exception('서비스 정보가 없습니다.')
        if not util.is_value('name', model):
            raise Exception('리소스명을 입력하세요.')
        
        result_data = sql.insert_resource(model)

        if result_data.resource_id :
            Response.message=''
            Response.data=[{"resource_id":result_data.resource_id}]
        else:
            raise Exception('리소스를 생성하는데 실패했습니다.')
        return Response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#리소스 정보 업데이트
@router.patch('/{resource_id}', response_model=Response)
async def update_service(resource_id:str, model: RequestDTO.Resource):
    try:
        if not resource_id:
            raise Exception('리소스를 찾을 수 없습니다.')
        if not util.is_value('name', model):
            raise Exception('리소스명을 입력하세요.')
        if not util.is_value('service_id', model):
            raise Exception('서비스를 찾을 수 없습니다.')

        result_data = sql.update_resource(resource_id, model)

        Response.message=''
        Response.data=[{"resource_id" : resource_id}]
        return Response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#f리소스 삭제
@router.delete('/{resource_id}', response_model=Response)
async def delete_resource(resource_id:str):
    try:
        if not resource_id:
            raise Exception('리소스를 찾을 수 없습니다.')
    
        result_data = sql.delete_resource(resource_id)

        if result_data == 0:
            raise Exception('리소스를 삭제하는데 실패했습니다.')

        Response.message=''
        return Response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())