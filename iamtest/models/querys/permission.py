from io import StringIO
from iamtest.models.entity import permission
from iamtest.commons import util

def select_permission(conn, data):
    try:
        query = f'''
            SELECT
                permission_id
                , service_id
                , resource_id
                , permission_name
                , permission
                , remark
            FROM
                permission
            {util.make_search_option(data, ['permission_name', 'remark'])} ;
        '''
        
        result = conn.query(query, param=data, model=permission.Permission)
        conn.connection.commit()
    except Exception as Err:
        print(Err)
        conn.connection.rollback()
    return result


def insert_permission(conn, data):
    try:
        insert_query  = util.make_insert_query('permission', data)
        select_query = ' SELECT @@IDENTITY AS permission_id; '

        conn.execute(insert_query, param=data)
        result = conn.query(select_query, param=data, model=permission.Permission)[0]
        conn.connection.commit()
    except Exception as Err:
        conn.connection.rollback()
        print("**********SQL EXECUTE ERROR********")
        print(Err)
    return result


def update_permission(conn, target_id, data):
    values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                permission
            SET 
                {values}
            WHERE
                permission_id = {target_id};
        '''
        
        result = conn.execute(query, param=data)
        conn.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        conn.connection.rollback()
    return result


def delete_permission(conn, target_id):
    try:
        query = '''
            DELETE FROM permission WHERE permission_id = ?permission_id?;
        '''
        #TODO : 할당되어있는 권한정보 삭제(user_permission, group_permission)
        
        result = conn.execute(query, param={'permission_id': target_id})
        conn.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        conn.connection.rollback()
    return result