from fastapi import APIRouter, HTTPException, Header, Request
from typing import Dict, Any, Union
import logging
from iamtest.commons import util
from iamtest.commons import config
import iamtest.models.querys.user as sql
from iamtest.models.entity.common import Response

router = APIRouter()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

@router.get('')
def select_info(request:Request):
    identity = request.headers.get("identity") #header의 사번
    db = config.db_connection()
    try:
        if not identity:
            raise Exception('사원정보가 없습니다.')
        result_data, total_count = sql.select_info(db, identity)

        response = util.make_response(result_data, total_count)
        logger.info(str(response), extra={'status_code':200}, exc_info=True)
        return response
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()
