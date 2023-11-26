from io import StringIO
from iamtest.models.entity import resource
from iamtest.commons import util

def select_resource(conn, data):
    try:
        query = f'''
            SELECT
                resource_id
                , service_id
                , name
                , remark
            FROM
                resource
            {util.make_search_option(data, ['name', 'remark'])} ;
        '''
        
        result = conn.query(query, param=data, model=resource.Resource)
        conn.connection.commit()
    except Exception as Err:
        print(Err)
        conn.connection.rollback()
    return result


def insert_resource(conn, data):
    try:
        insert_query  = util.make_insert_query('resource', data)
        select_query = ' SELECT @@IDENTITY AS resource_id; '

        conn.execute(insert_query, param=data)
        result = conn.query(select_query, param=data, model=resource.Resource)[0]

        conn.connection.commit()
    except Exception as Err:
        conn.connection.rollback()
        print(Err)
        print("**********SQL EXECUTE ERROR********")
    return result


def update_resource(conn, target_id, data):
    values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                resource
            SET 
                {values}
            WHERE
                resource_id = {target_id};
        '''
        
        print(query)
        result = conn.execute(query, param=data)
        conn.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        conn.connection.rollback()
    return result


def delete_resource(conn, target_id):
    try:
        query = '''
            DELETE FROM resource WHERE resource_id = ?resource_id?;
        '''
        result = conn.execute(query, param={'resource_id': target_id})
        conn.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        conn.connection.rollback()
    return result