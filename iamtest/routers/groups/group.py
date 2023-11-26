from fastapi import APIRouter
from iamtest.models.entity.model import Response
from iamtest.commons import util 
import iamtest.models.requests.group as RequestDTO
import iamtest.commons.config as config
import iamtest.models.querys.group as sql

router = APIRouter()
db_conn = config.db_connection()

#권한그룹 목록 조회
@router.get('/list', response_model=Response)
def select_group(model: RequestDTO.Group | None = None):
    try:
        result_data = sql.select_group(db_conn, model)
        
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

#권한그룹 생성
@router.post('/save', response_model=Response)
async def insert_group(model: RequestDTO.Group):
    try:
        if not util.is_value('group_name', model):
            raise Exception('그룹명을 입력하세요.')
        
        result_data = sql.insert_group(db_conn, model)

        if result_data.group_id :
            return select_group(model=RequestDTO.Group(group_id=str(result_data.group_id))) 
        else:
            raise Exception('권한그룹을 생성하는데 실패했습니다.')

    except Exception as err_msg:
        return Response(
            Result='Error',
            Code='9999',
            Message=str(err_msg),
            Data=[]
        )

#권한그룹 정보 수정
@router.patch('/update/{group_id}', response_model=Response)
async def update_service(group_id:str, model: RequestDTO.Group):
    try:
        if not group_id:
            raise Exception('권한그룹을 찾을 수 없습니다.')
        if not util.is_value('group_name', model):
            raise Exception('그룹명을 입력하세요.')
    
        result_data = sql.update_group(db_conn, group_id, model)

        #update완료된 경우
        if result_data != 0:
            return select_group(model=RequestDTO.Group(group_id=group_id))

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

#권한그룹 삭제
@router.delete('/delete/{group_id}', response_model=Response)
async def delete_group(group_id:str):
    try:
        if not group_id:
            raise Exception('권한그룸을 찾을 수 없습니다.')
    
        result_data = sql.delete_group(db_conn, group_id)

        if result_data == 0:
            raise Exception('권한그룹을 삭제하는데 실패했습니다.')
        
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
