#공통함수
from pydantic import BaseModel

def make_insert_query(table:str, model:BaseModel):
    try:
        model = model.dict(exclude_unset=True)
        
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

def make_search_option(model, search_options):
    if model:
        model = model.dict(exclude_unset=True)
        entity_colums = ''
        options = ''
        try:
            for key in model:
                if entity_colums:
                    entity_colums += ' AND '
                if key == 'search' and len(search_options) > 0:
                    for option in search_options:
                        if options:
                            options += ' OR '
                        else:
                            options = ' ( '
                        options += option + ' LIKE ?' + key + '?'
                    options += ')'
                    entity_colums += options
                else:
                    entity_colums += key + '=?' + key + '?'
        except Exception as err_msg:
            raise Exception('쿼리문 생성 오류' + err_msg)
        if entity_colums:
            return 'WHERE ' + entity_colums
        else:
            return ''
    else:
        return ''

def make_entity_colums(model:BaseModel):
    model = model.dict(exclude_unset=True)
    entity_colums = ''
    for key in model:
        if entity_colums:
            entity_colums += ', '
        entity_colums += key + '=?' + key + '?'
    return entity_colums

#model에 해당 key값이 빈값인지 체크
def is_value(key:str, model:BaseModel):
    model = model.dict(exclude_unset=True)
    if (key in model) and (not model.get(key)):
        return False
    else:
        return True