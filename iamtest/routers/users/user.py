from fastapi import APIRouter, HTTPException, Header
from typing import Dict, Any
import json
from iamtest.commons import util 
import iamtest.models.querys.user as sql
from iamtest.models.entity.common import response as Response

router = APIRouter()

@router.get('/', response_model=Response)
def select_info(identity: str = Header(default=None)):
    try:
        result_data = sql.select_info(identity)

        response = Response()
        response.data=[dict(data) for data in result_data]
        return response
    except Exception as error:
        response = Response(cdoe='', message=str(error))
        raise HTTPException(status_code=404, detail=response.dict())