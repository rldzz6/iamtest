from fastapi import APIRouter, HTTPException, Depends, Header, Request
from typing import Dict, Any
from datetime import datetime
import logging
from didimiam.commons import util 
from didimiam.commons import config
import didimiam.models.querys.resource as sql
import didimiam.models.requests.resource as RequestDTO
from didimiam.models.entity.common import Response
from didimiam.models.entity.common import Errorlog as Errorlog

router = APIRouter()
category = '리소스 관리'
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#리소스 목록 조회
@router.get('')
@router.get('/{resource_id}')
def select_resource(request:Request, page: int = 0, model: RequestDTO.Resource = Depends()):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        result_data = sql.select_resource(db, model, page)
        total_count = sql.select_resource_count(db, model)
        
        response = util.make_response(result_data, total_count[0])
        util.log(category, '리소스 정보 조회', model, identity)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#리소스 생성
@router.post('')
async def insert_resource(request:Request, model: RequestDTO.Resource):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        if not util.is_value('service_id', model) or util.is_empty('service_id', model):
            raise Exception('서비스 정보가 없습니다.')
        if not util.is_value('resource_name', model) or util.is_empty('resource_name', model):
            raise Exception('리소스명을 입력하세요.')
        
        result_data = sql.insert_resource(db, model)

        if not result_data :
            raise Exception('리소스를 생성하는데 실패했습니다.')

        util.log(category, '리소스 생성', model, identity)
        response = Response(data={"resource_id":result_data}, total_count=1)
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#리소스 정보 업데이트
@router.patch('/{resource_id}')
async def update_service(request:Request, resource_id:str, model: RequestDTO.Resource):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        if not resource_id:
            raise Exception('리소스를 찾을 수 없습니다.')
        if util.is_empty('resource_name', model):
            raise Exception('리소스명을 입력하세요.')
        if util.is_empty('service_id', model):
            raise Exception('서비스를 찾을 수 없습니다.')

        result = sql.update_resource(db, resource_id, model)

        util.log(category, '리소스 정보 수정', model, identity)
        response = Response(data={"resource_id" : resource_id})
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()

#f리소스 삭제
@router.delete('/{resource_id}')
async def delete_resource(request:Request, resource_id:str):
    identity = request.headers.get("identity")
    db = config.db_connection()
    try:
        model = RequestDTO.Resource(resource_id=resource_id)
        if not resource_id:
            raise Exception('리소스를 찾을 수 없습니다.')
    
        result_count = sql.delete_resource(db, resource_id)

        #if result_count == 0:
        #    raise Exception('리소스를 삭제하는데 실패했습니다.')

        util.log(category, '리소스 삭제', model, identity)
        response = Response()
        return response
    except Exception as error:
        logger.error(str(error), extra={'status_code': 500}, exc_info=True)
        raise HTTPException(status_code=500, detail=(Response(code='', message=str(error))).dict())
    finally:
        db.close()