from fastapi import APIRouter
import requests
import re
from fastapi import FastAPI, Request, HTTPException
from mangum import Mangum
from datetime import datetime
import logging
from pydantic import BaseModel
from datetime import datetime
from iamtest.commons import config
from iamtest.models.entity.common import Log
from iamtest.models.entity.common import Response
from iamtest.models.entity.common import Errorlog

page_unit = 20

app = FastAPI()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#작업자 IP주소 조회
def get_ip():
    req = requests.get("http://ipconfig.kr")
    out_addr = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]
    return out_addr

def log_description(basemodel, logmodel):
    #none값 제거
    data = basemodel.dict(exclude_none=True)
    description = ""
    for key in data:
        description += logmodel.get(key) + ' : "' + str(data.get(key)).replace("'", "") + '"  '
    return description


#로그 저장 (카테고리, 작업내용, 요청파라미터, 사번, 비고)
def log(category, action, description, employee_id, remark=''):
    if remark:
        description += '\n' + remark

    #log 모델 생성
    log = Log(
        category = category
        , action = action
        , description = description
        , action_time = str(datetime.now())
        , employee_id = employee_id
        , ip = get_ip()
    )

    #log INSERT
    try:
        db = config.db_connection()
        insert_query = make_insert_query('iam_log', log)
        #insert_query = f''' INSERT iam_log ( category, description, action, action_time, employee_id, ip ) 
        #                    VALUES ('{log.category}', '{log.description}', '{log.action}', '{log.action_time}', '{log.employee_id}', '{log.ip}' ); '''
       
        with db.cursor() as cur:
            cur.execute(insert_query)
            db.commit()
    except Exception as error:
        raise(error)

#에러 로그 생성
def exception_log(request: Request, exc: Exception, status: int = 500):
    identity = request.headers.get("identity")
    error_msg = Errorlog(identity=identity, url_path=str(request.url), asc_time=str(datetime.now()), status=str(status), level='ERROR', message=str(exc))
    logger.error(str(error_msg.dict()), extra={'status_code': status}, exc_info=True)
    return Response(message=str(exc))

#INSERT문 쿼리 생성
def make_insert_query(table:str, model:BaseModel):
    try:
        model = model.dict(exclude_unset=True, exclude_none=True)
        
        #model을 기반으로 쿼리문 생성
        columns = ''
        values = ''
        for key in model:
            if columns:
                columns += ', '
                values += ', '
            columns += key
            values += "'" + model.get(key) + "'"
        
        if not columns or not values:
            raise Exception('쿼리문 생성 오류')
        
        result = ' INSERT `' + table
        result += '` ( ' + columns + ' ) '
        result += 'VALUES (' + values + ' ); '
    except Exception as err_msg:
        raise Exception(err_msg)
    return result

#SELECT문 WHERE 옵션 생성
def make_search_option(model, search_options):
    if model:
        model = model.dict(exclude_unset=True, exclude_none=True)
        entity_colums = ''
        option_colums = ''
        try:
            for key in model:
                if entity_colums:
                    entity_colums += ' AND '
                if key == 'keyword' and len(search_options) > 0:
                    for option in search_options:
                        if option_colums:
                            option_colums += ' OR '
                        else:
                            option_colums = ' ( '
                        option_colums += ' LOCATE(?' + key + '?, ' + option + ') > 0 '
                    option_colums += ')'
                    entity_colums += option_colums
                else:
                    entity_colums += key + '=?' + key + '?'
        except Exception as err_msg:
            raise Exception('쿼리문 생성 오류' + err_msg)
        if entity_colums:
            return 'AND ' + entity_colums
        else:
            return ''
    else:
        return ''

#SELECT문 pagination옵션 생성 (페이지번호, 출력갯수)
def pagination(page):
    page -= 1
    # page_no = -1인 경우 전체 리스트 호출
    if page == -1:
        return ';'
    else:
        return ' LIMIT {},{} ;'.format(page_unit * page, page_unit)

#UPDATE문 SET옵션 생성
def make_entity_colums(model:BaseModel):
    model = model.dict(exclude_unset=True, exclude_none=True)
    entity_colums = ''
    for key in model:
        if entity_colums:
            entity_colums += ', '
        entity_colums += key + "='" + model.get(key).replace("'","") + "'"
    if not entity_colums:
        raise Exception('쿼리문 생성 오류 : 업데이트 값이 없습니다.')
    return entity_colums

#model에 해당 key값을 전달받았는지 체크
def is_value(key:str, model:BaseModel):
    model = model.dict(exclude_unset=True, exclude_none=True)
    if not model:
        return False
    elif key not in model:
        return False
    elif not model.get(key):
        return False
    else:
        return True

#model에 해당 key값이 빈값인지 체크
def is_empty(key:str, model:BaseModel):
    model = model.dict(exclude_unset=True, exclude_none=True)
    if not model:
        return True
    elif (key in model) and (not model.get(key)):
        return True
    else:
        return False

#페이지 갯수 계산
def get_total_page(total_count, view_count):
    if total_count % view_count == 0:
        return total_count // view_count
    else:
        return total_count // view_count + 1

#result data를 response 형태로 변환
def make_response(result_data, total_count=1):
    if len(result_data) == 0:
        response_data = None
    else:
        response_data = [data._asdict() for data in result_data]

    response = Response(data=response_data, total_count=total_count, total_page=get_total_page(total_count, page_unit))
    return response
