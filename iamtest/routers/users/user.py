from fastapi import APIRouter, HTTPException, Header, Request
from typing import Dict, Any, Union
from iamtest.commons import util 
import iamtest.models.querys.user as sql
from iamtest.models.entity.common import Response

router = APIRouter()

@router.get('')
def select_info(request:Request):
    identity = request.headers.get("identity") #header의 사번
    try:
        if not identity:
            raise Exception('사원정보가 없습니다.')
        result_data = sql.select_info(identity)

        response = Response(data=result_data.dict())
        return response
    except Exception as error:
        status_code = 400
        response = util.exception_log(request=request, exc=error, status=status_code)
        raise HTTPException(status_code=status_code, detail=response.dict())
