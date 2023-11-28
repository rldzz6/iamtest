from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any
from iamtest.models.entity.model import Response
from iamtest.commons import util 
import iamtest.models.requests.permission as RequestDTO
import iamtest.commons.config as config
import iamtest.models.querys.permission as sql

router = APIRouter()
db_conn = config.db_connection()

@router.get('/list', response_model=Response)
def select_permission(permission_id: str | None = None, service_id: str | None = None, resource_id: str | None = None, name: str | None = None, search: str | None = None):
    try:
        model = RequestDTO.Permission()
        model.permission_id = permission_id
        model.service_id = service_id
        model.resource_id = resource_id
        model.permission_name = name
        model.search = search
        result_data = sql.select_permission(db_conn, model)
        
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
async def insert_permission(model: RequestDTO.Permission):
    try:
        if not util.is_value('service_id', model):
            raise Exception('서비스 정보가 없습니다.')
        if not util.is_value('resource_id', model):
            raise Exception('리소스 정보가 없습니다.')
        if not util.is_value('permission_name', model):
            raise Exception('권한명을 입력하세요.')
        if not util.is_value('permission', model):
            raise Exception('권한을 선택하세요.')
        if model.permission == '0':
            raise Exception('권한을 선택하세요')
        
        result_data = sql.insert_permission(db_conn, model)

        if result_data.permission_id :
            return select_permission(permission_id=str(result_data.permission_id)) 
        else:
            raise Exception('권한을 생성하는데 실패했습니다.')

    except Exception as err_msg:
        return Response(
            Result='Error',
            Code='9999',
            Message=str(err_msg),
            Data=[]
        )

@router.patch('/update/{permission_id}', response_model=Response)
async def update_service(permission_id:int, model: RequestDTO.Permission):
    try:
        if not permission_id:
            raise Exception('권한 정보를 찾을 수 없습니다.')
        if not util.is_value('service_id', model):
            raise Exception('서비스 정보가 없습니다.')
        if not util.is_value('resource_id', model):
            raise Exception('리소스 정보가 없습니다.')
        if not util.is_value('permission_name', model):
            raise Exception('권한명을 입력하세요.')
        if not util.is_value('permission', model):
            raise Exception('권한을 선택하세요.')
        if model.permission == '0':
            raise Exception('권한을 선택하세요')
        result_data = sql.update_permission(db_conn, permission_id, model)

        #update완료된 경우
        if result_data != 0:
            return select_permission(permission_id=permission_id)

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

@router.delete('/delete/{permission_id}', response_model=Response)
async def delete_permission(permission_id:int):
    try:
        if not permission_id:
            raise Exception('권한을 찾을 수 없습니다.')
    
        result_data = sql.delete_permission(db_conn, permission_id)

        if result_data == 0:
            raise Exception('권한을 삭제하는데 실패했습니다.')
        
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
