from io import StringIO
from iamtest.models.entity import service
from iamtest.commons import util

def select_service(conn, data):
    try:
        query = '''
            SELECT
                id AS service_id
                , service_name
                , service_url
            FROM
                service
            WHERE
                ?service_id? = '' OR id = ?service_id?;
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

        print(query)
        
        result = conn.execute(query, param=data)
        conn.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        conn.connection.rollback()
    return result


def update_service(conn, target_id, data):
    values = util.make_entity_colums(data)
    print(data)
    try:
        query = f'''
            UPDATE
                service
            SET 
                {values}
            WHERE
                id = {target_id};
        '''
        
        print(query)
        result = conn.execute(query, param=data)
        conn.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        conn.connection.rollback()
    return result


def delete_service(conn, data):
    try:
        query = '''
            DELETE FROM service WHERE id = ?service_id?;
        '''
        result = conn.execute(query, param=data)
        conn.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        conn.connection.rollback()
    return result