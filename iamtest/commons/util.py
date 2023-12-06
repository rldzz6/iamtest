from pydantic import BaseModel
from datetime import datetime
import iamtest.commons.config as config
from iamtest.models.entity.common import Log

page_unit = 20

def log(category, work_type, rmk, request_body, status, employee_id, error_msg = ''):
    
    description = rmk
    if request_body:
        description += '\n' + str(request_body.dict(exclude_none=True))
    if error_msg:
        description += '\n' + '**error msg :' + error_msg
    
    log = Log()
    log.category = category
    log.description = description
    log.work_type = work_type
    log.work_status = status
    log.work_time = str(datetime.now())
    log.employee_id = employee_id
    log.work_ip = ''
    
    try:
        db = config.db_connection()
        insert_query = make_insert_query('iam_log', log)

        db.execute(insert_query, param=log)
        db.connection.commit()
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

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
            values += '?' + key + '?'
        
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
                if key == 'page_no': continue
                if entity_colums:
                    entity_colums += ' AND '
                if key == 'search' and len(search_options) > 0:
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
        entity_colums += key + '=?' + key + '?'
    if not entity_colums:
        raise Exception('쿼리문 생성 오류 : 업데이트 값이 없습니다.')
    return entity_colums

#model에 해당 key값이 빈값인지 체크
def is_value(key:str, model:BaseModel):
    model = model.dict(exclude_unset=True, exclude_none=True)
    if not model:
        return False
    elif (key in model) and (not model.get(key)):
        return False
    else:
        return True