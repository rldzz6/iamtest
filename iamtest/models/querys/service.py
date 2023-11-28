from io import StringIO
from iamtest.models.entity import service
from iamtest.commons import util

def select_service(conn, data):
    try:
        query = f'''
            SELECT
                service_id
                , service_name
                , service_url
            FROM
                service
            {util.make_search_option(data, ['service_name', 'service_url'])} ;
        '''
        
        result = conn.query(query, param=data, model=service.Service)
        conn.connection.commit()
    except Exception as Err:
        print(Err)
        conn.connection.rollback()
    return result


def insert_service(conn, data):
    try:
        query  = util.make_insert_query('service', data)

        result = conn.execute(query, param=data)
        conn.connection.commit()
    except Exception as Err:
        conn.connection.rollback()
        print("**********SQL EXECUTE ERROR********")
        print(Err)
    return result


def update_service(conn, target_id, data):
    values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                service
            SET 
                {values}
            WHERE
                service_id = {target_id};
        '''
        
        result = conn.execute(query, param=data)
        conn.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        conn.connection.rollback()
    return result


def delete_service(conn, target_id):
    try:
        query = '''
            DELETE FROM service WHERE service_id = ?service_id?;
        '''
        #TODO : 서비스 하위 리소스 및 권한 삭제
        
        result = conn.execute(query, param={'service_id': target_id})
        conn.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        conn.connection.rollback()
    return result