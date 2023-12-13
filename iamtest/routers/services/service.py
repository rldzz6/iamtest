from fastapi import APIRouter, HTTPException, Depends, Header, Request
from typing import Dict, Any
from datetime import datetime
import json, logging
from didimiam.commons import util
from didimiam.commons import config
import didimiam.models.querys.service as sql
import didimiam.models.requests.service as RequestDTO
from didimiam.models.entity.common import Response

router = APIRouter()
category = '서비스 관리'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#서비스 정보 조회
@router.get('')
@router.get('/{service_id}')
def select_service(request:Request, page: int = 0, model: RequestDTO.Service = Depends()):
    identity = request.headers.get("identity") #header의 사번
    db = config.db_connection()
    try:
        result_data = sql.select_service(db, model, page)
        total_count = sql.select_service_count(db, model)
        
        response = util.make_response(result_data, total_count[0])
        util.log(category, '서비스 정보 조회', model, identity)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#서비스 생성
@router.post('')
async def insert_service(request:Request, model: RequestDTO.Service):
    identity = request.headers.get("identity") #header의 사번
    db = config.db_connection()
    try:
        if not util.is_value('service_name', model) or util.is_empty('service_name', model):
            raise Exception('서비스명을 입력하세요.')

        result_data = sql.insert_service(db, model)

        if not result_data :
            raise Exception('서비스를 생성하는데 실패했습니다.')

        util.log(category, '서비스 생성', model, identity)
        response = Response(data={"service_id":result_data}, total_count=1)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#서비스 정보 업데이트
@router.patch('/{service_id}')
async def update_service(request:Request, service_id:str, model: RequestDTO.Service):
    identity = request.headers.get("identity") #header의 사번
    db = config.db_connection()
    try:
        if not service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
        if util.is_empty('service_name', model):
            raise Exception('서비스명을 입력하세요.')

        result = sql.update_service(db, service_id, model)
        
        util.log(category, '서비스 정보 수정', model, identity)
        response = Response(data={"service_id" : service_id})
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

@router.delete('/{service_id}')
async def delete_service(request:Request, service_id:str):
    identity = request.headers.get("identity") #header의 사번
    db = config.db_connection()
    try:
        model = RequestDTO.Service(service_id=service_id)
        if not service_id:
            raise Exception('서비스를 찾을 수 없습니다.')
    
        result_count = sql.delete_service(db, service_id)

        #if result_count == 0:
        #    raise Exception('서비스를 삭제하는데 실패했습니다.')
        
        util.log(category, '서비스 삭제', model, identity)
        response = Response()
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()