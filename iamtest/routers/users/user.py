from fastapi import APIRouter, HTTPException, Header, Request
from typing import Dict, Any, Union
import logging
from didimiam.commons import util
from didimiam.commons import config
import didimiam.models.querys.user as sql
from didimiam.models.entity.common import Response

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
        result_data = sql.select_info(db, identity)

        response = util.make_response(result_data)
        return response
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()
