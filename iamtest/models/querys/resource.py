from io import StringIO
from iamtest.commons import util
from iamtest.commons import config
from iamtest.models.entity import resource

#리소스 목록 조회
def select_resource(data, page_no):
    db = config.db_connection()
    search_option = util.make_search_option(data, ['resource_name', 'remark'])
    try:
        query = f'''
            SELECT
                resource_id
                , service_id
                , resource_name
                , remark
            FROM
                resource
            WHERE
                1 = 1
        ''' 
        query += search_option
        query += util.pagination(page_no)      

        if search_option != '':
            result = db.query(query, param=data, model=resource.Resource)
        else:
            result = db.query(query, model=resource.Resource)
        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#리소스 전체 갯수 조회
def select_resource_count(data):
    db = config.db_connection()
    search_option = util.make_search_option(data, ['resource_name', 'remark'])
    try:
        query = f'''
            SELECT
                COUNT(*) AS count
            FROM
                resource
            WHERE
                1 = 1
        ''' 
        query += search_option

        if search_option != '':
            result = db.execute_scalar(query, param=data)
        else:
            result = db.execute_scalar(query)
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#리소스 생성
def insert_resource(data):
    db = config.db_connection()
    try:
        insert_query = util.make_insert_query('resource', data)
        select_query = 'SELECT @@IDENTITY AS resource_id;'

        db.execute(insert_query, param=data)
        result = db.query_first(select_query, model=resource.Resource)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#리소스 정보 수정
def update_resource(target_id, data):
    db = config.db_connection()
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                resource
            SET 
                {update_values}
            WHERE
                resource_id = {target_id};
        '''
        
        result = db.execute(query, param=data)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#리소스 삭제
def delete_resource(target_id):
    db = config.db_connection()
    try:
        query = '''
            DELETE FROM resource WHERE resource_id = ?resource_id?;
        '''
        #TODO : 리소스 하위 권한 삭제
        
        result = db.execute(query, param={'resource_id': target_id})
        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)
