from fastapi import APIRouter
from fastapi.responses import JSONResponse
from iamtest.models.entity.model import response
from iamtest.commons import util 
import iamtest.models.requests.group as RequestDTO
import iamtest.models.querys.group as sql

router = APIRouter()

#권한그룹 목록 조회
@router.get('/', response_model=response)
@router.get('/{group_id}', response_model=response)
def select_group(group_id: str | None = None, model: RequestDTO.Group | None = None):
    print(model)
    try:
        model.group_id = group_id
        result_data = sql.select_group(model)

        response.message=''
        response.data=[dict(data) for data in result_data]

        return response
    except Exception as err_msg:
        response.message=err_msg
        return response

#권한그룹 생성
@router.post('/', response_model=response)
async def insert_group(model: RequestDTO.Group):
    try:
        if not util.is_value('group_name', model):
            raise Exception('그룹명을 입력하세요.')
        
        result_data = sql.insert_group(model)

        if result_data.group_id :
            response.message=''
            response.data=[{"group_id":result_data.group_id}]
        else:
            raise Exception('권한그룹을 생성하는데 실패했습니다.')

        return response
    except Exception as err_msg:
        raise JSONResponse(
            status_code=418,
            content={"message": err_msg},
        )

#권한그룹 정보 수정
@router.patch('/{group_id}', response_model=response)
async def update_service(group_id:str, model: RequestDTO.Group):
    try:
        if not group_id:
            raise Exception('권한그룹을 찾을 수 없습니다.')
        if not util.is_value('group_name', model):
            raise Exception('그룹명을 입력하세요.')
    
        result_data = sql.update_group(group_id, model)

        response.message=''
        return response
    except Exception as err_msg:
        response.message=err_msg
        return response

#권한그룹 삭제
@router.delete('/{group_id}', response_model=response)
async def delete_group(group_id:str):
    try:
        if not group_id:
            raise Exception('권한그룸을 찾을 수 없습니다.')
    
        result_data = sql.delete_group(group_id)

        if result_data == 0:
            raise Exception('권한그룹을 삭제하는데 실패했습니다.')

        response.message=''
        return response
    except Exception as err_msg:
        response.message=err_msg
        return response
