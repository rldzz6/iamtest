from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any
import json
from iamtest.models.entity.model import Response
from iamtest.commons import util 
import iamtest.models.requests.service as Request
import iamtest.commons.config as config
import iamtest.models.querys.service as sql

router = APIRouter()
db_conn = config.db_connection()

@router.get('/list', response_model=Response)
async def select_service(service_id: int | None = ''):
    model = Request.Service();
    model.service_id = service_id
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
async def insert_service(Request: Request.Service):
    try:
        if not util.is_value('service_name', Request):
            raise Exception('서비스명을 입력하세요.')

        result_data = sql.insert_service(db_conn, Request)

        if result_data == 0:
            raise Exception('서비스를 저장하는데 실패했습니다.')

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

@router.patch('/update', response_model=Response)
async def update_service(service_id:str, model: Request.Service):
    try:
        if not service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
        if not util.is_value('service_name', model):
            raise Exception('서비스명을 입력하세요.')
    
        result_data = sql.update_service(db_conn, service_id, model)

        if result_data == 0:
            raise Exception('서비스를 저장하는데 실패했습니다.')
        
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

@router.delete('/delete', response_model=Response)
async def delete_service(model: Request.Service):
    try:
        if not model.service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
    
        result_data = sql.delete_service(db_conn, model)

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

'''
@router.get('/tt')
def read_item():
    db_conn = config.db_connection()
    print("***************************")
    query = "SELECT id, service_name, service_url FROM service"
    with db_conn.cursor() as cursor:
        cursor.execute(query)
        item = cursor.fetchall()
        cursor.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/tt_insert")
def create_item(item: request):
    try:
        print(item.service_name)
        print(item.service_url)
        db_conn = config.db_connection()
        query = "INSERT INTO `service` (service_name, service_url) VALUES (%s, %s)"

        with db_conn.cursor() as cursor:
            cursor.execute(query, (item.service_name, item.service_url))
            item = cursor.fetchall()
            cursor.close()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        db_conn.commit()
    except Exception as exc:
        print(exc)

    return item



@router.get('/list', response_model=Response)
async def get_service(service_id: int | None = ''):
    try:
        parameter_model = request()
        parameter_model.service_id = service_id
        db_conn = config.db_connection()
        result_data = sql.select_service(db_conn, parameter_model)
        print('***************************')
        print(result_data)
        #print(**result_data.dict())
        print('***************************')
        print([dict(data) for data in result_data])
    except Exception as err_msg:
        print(err_msg)
    finally:
        return Response(
                Result='OK',
                Code='0000',
                Message='',
                Data=[]
        )

@router.get('/list_model/', response_model=Response)
async def get_service(model: request):
    print(model)
    try:
        db_conn = config.db_connection()
        result_data = sql.select_service(db_conn, model)
        print('***************************')
        print(**result_data.dict())
        print('***************************')
        print([dict(data) for data in result_data])
    except Exception as err_msg:
        print(err_msg)
    finally:
        return Response(
                Result='OK',
                Code='0000',
                Message='',
                Data=[]
        )
        '''