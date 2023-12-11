from fastapi import APIRouter, HTTPException, Depends, Header, Request
from fastapi.responses import JSONResponse
from iamtest.commons import util
import iamtest.models.querys.group as sql
import iamtest.models.requests.group as RequestDTO
from iamtest.models.entity.common import Response

router = APIRouter()
category = '권한그룹 관리'

#권한그룹 정보 조회
@router.get('')
@router.get('/{group_id}')
def select_group(request:Request, page: int = 0, model: RequestDTO.Group = Depends()):
    identity = request.headers.get("identity")
    try:
        result_data = sql.select_group(model, page)
        total_count = sql.select_group_count(model)

        response = util.make_response(result_data, total_count)   
        util.log(category, '권한그룹 정보 조회', model, identity)
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#권한그룹 생성
@router.post('')
async def insert_group(request:Request, model: RequestDTO.Group):
    identity = request.headers.get("identity")
    try:
        if not util.is_value('group_name', model) or util.is_empty('group_name', model):
            raise Exception('그룹명을 입력하세요.')
        
        result_data = sql.insert_group(model)

        if not result_data.group_id :
            raise Exception('권한그룹을 생성하는데 실패했습니다.')

        response = Response(data={"group_id":result_data.group_id}, total_count=1)
        util.log(category, '권한그룹 생성', model, identity)
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#사용자 목록
@router.get('/{group_id}/user')
def select_group_user(request:Request, group_id: str):
    identity = request.headers.get("identity")
    try:
        result_data = sql.select_group_user(group_id)

        response = Response()
        response.data=[data.dict(exclude_unset=True, exclude_none=True) for data in result_data]
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#권한 목록
@router.get('/{group_id}/permission')
def select_group_permission(request:Request, group_id: str, page:int = 0, model: RequestDTO.Permission = Depends()):
    identity = request.headers.get("identity")
    try:
        result_data = sql.select_group_permission(group_id, model, page)
        result_count = sql.select_group_permission_count(group_id, model)

        response = Response(data=result_data
                    , total_count=int(result_count)
                    , total_page=util.get_total_page(int(result_count), util.page_unit))
        return response
    except Exception as error:
        response = Response(code='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())

#권한그룹 정보 수정
@router.patch('/{group_id}')
async def update_service(request:Request, group_id:str, model: RequestDTO.Group):
    identity = request.headers.get("identity")
    try:
        if not group_id:
            raise Exception('권한그룹을 찾을 수 없습니다.')
        if util.is_empty('group_name', model):
            raise Exception('그룹명을 입력하세요.')

        result_count = sql.update_group(group_id, model)

        util.log(category, '권한그룹 정보 수정', model, identity)

        response = Response(data={"group_id" : group_id}, total_count=int(result_count))
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())

#권한그룹 삭제
@router.delete('/{group_id}')
async def delete_group(request:Request, group_id:str):
    identity = request.headers.get("identity")
    try:
        model = RequestDTO.Group(group_id=group_id)
        if not group_id:
            raise Exception('권한그룹을 찾을 수 없습니다.')
    
        result_count = sql.delete_group(group_id)

        if result_count == 0:
            raise Exception('권한그룹을 삭제하는데 실패했습니다.')

        util.log(category, '권한그룹 삭제', model, identity)
        response = Response(total_count=int(result_count))
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())
