from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any
import json
from iamtest.models.entity.model import Response
from iamtest.commons import util 
import iamtest.models.requests.service as RequestDTO
import iamtest.commons.config as config
import iamtest.models.querys.service as sql

router = APIRouter()
db_conn = config.db_connection()

@router.get('/list/', response_model=Response)
def select_service(model: RequestDTO.Service | None = None):
    try:
        result_data = sql.select_service(db_conn, model)
        
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

@router.post('/save', response_model=Response)
async def insert_service(model: RequestDTO.Service):
    try:
        if not util.is_value('service_name', model):
            raise Exception('서비스명을 입력하세요.')

        result_data = sql.insert_service(db_conn, model)

        if result_data == 0:
            raise Exception('서비스를 생성하는데 실패했습니다.')

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

@router.patch('/update/{service_id}', response_model=Response)
async def update_service(service_id:str, model: RequestDTO.Service):
    try:
        if not service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
        if not util.is_value('service_name', model):
            raise Exception('서비스명을 입력하세요.')
    
        result_data = sql.update_service(db_conn, service_id, model)

        #update완료된 경우
        if result_data != 0:
            return select_service(model=RequestDTO.Service(service_id=service_id))

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

@router.delete('/delete/{service_id}', response_model=Response)
async def delete_service(service_id:str):
    try:
        if not service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
    
        result_data = sql.delete_service(db_conn, service_id)

        if result_data == 0:
            raise Exception('서비스를 삭제하는데 실패했습니다.')
        
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
