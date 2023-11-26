from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any
import json
from iamtest.models.entity.model import Response
from iamtest.commons import util 
import iamtest.models.requests.resource as RequestDTO
import iamtest.commons.config as config
import iamtest.models.querys.resource as sql

router = APIRouter()
db_conn = config.db_connection()

@router.get('/list', response_model=Response)
def select_resource(model: RequestDTO.Resource | None = None):
    try:
        result_data = sql.select_resource(db_conn, model)
        
        return Response(
            Result='OK',
            Code='0000',
            Message='',
            Data=[dict(data) for data in result_data]
        )
    except Exception as err_msg:
        return Response(
            Result='Error',
            Code='9999',
            Message=str(err_msg),
            Data=[]
        )

@router.post('/save/', response_model=Response)
async def insert_resource(model: RequestDTO.Resource):
    try:
        if not util.is_value('service_id', model):
            raise Exception('서비스 정보가 없습니다.')
        if not util.is_value('name', model):
            raise Exception('리소스명을 입력하세요.')
        
        result_data = sql.insert_resource(db_conn, model)

        if result_data.resource_id :
            return select_resource(model=RequestDTO.Resource(resource_id=str(result_data.resource_id))) 
        else:
            raise Exception('리소스를 저장하는데 실패했습니다.')

    except Exception as err_msg:
        return Response(
            Result='Error',
            Code='9999',
            Message=str(err_msg),
            Data=[]
        )

@router.patch('/update/{resource_id}', response_model=Response)
async def update_service(resource_id:str, model: RequestDTO.Resource):
    try:
        if not resource_id:
            raise Exception('리소스를 찾을 수 없습니다.')
        if not util.is_value('name', model):
            raise Exception('리소스명을 입력하세요.')
    
        result_data = sql.update_resource(db_conn, resource_id, model)

        #update완료된 경우
        if result_data != 0:
            return select_resource(model=RequestDTO.Resource(resource_id=resource_id))

        return Response(
            Result='OK',
            Code='0000',
            Message='',
            Data=[]
        )
    except Exception as err_msg:
        return Response(
            Result='Error',
            Code='9999',
            Message=str(err_msg),
            Data=[]
        )

@router.delete('/delete/{resource_id}', response_model=Response)
async def delete_resource(resource_id:str):
    try:
        if not resource_id:
            raise Exception('리소스를 찾을 수 없습니다.')
    
        result_data = sql.delete_resource(db_conn, resource_id)

        if result_data == 0:
            raise Exception('리소스를 삭제하는데 실패했습니다.')
        
        return Response(
            Result='OK',
            Code='0000',
            Message='',
            Data=[]
        )
    except Exception as err_msg:
        return Response(
            Result='Error',
            Code='9999',
            Message=str(err_msg),
            Data=[]
        )
