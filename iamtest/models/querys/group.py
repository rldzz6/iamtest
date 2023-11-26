from io import StringIO
from iamtest.models.entity import group
from iamtest.commons import util

def select_group(conn, data):
    try:
        query = f'''
            SELECT
                group_id
                , group_name
                , remark
            FROM
                `group`
            {util.make_search_option(data, ['group_name', 'remark'])} ;
        '''
        
        result = conn.query(query, param=data, model=group.Group)
        conn.connection.commit()
    except Exception as Err:
        print(Err)
        conn.connection.rollback()
    return result

def insert_group(conn, data):
    try:
        insert_query  = util.make_insert_query('group', data)
        select_query = ' SELECT @@IDENTITY AS group_id; '

        conn.execute(insert_query, param=data)
        result = conn.query(select_query, param=data, model=group.Group)[0]

        conn.connection.commit()
    except Exception as Err:
        conn.connection.rollback()
        print(Err)
        print("**********SQL EXECUTE ERROR********")
    return result

def update_group(conn, target_id, data):
    values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                `group`
            SET 
                {values}
            WHERE
                group_id = {target_id};
        '''
        
        result = conn.execute(query, param=data)
        conn.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        conn.connection.rollback()
    return result

def delete_group(conn, target_id):
    try:
        query = '''
            DELETE FROM `group` WHERE group_id = ?group_id?;
        '''
        #TODO : 권한그룹에 할당된 권한 삭제
        
        result = conn.execute(query, param={'group_id': target_id})
        conn.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        conn.connection.rollback()
    return result