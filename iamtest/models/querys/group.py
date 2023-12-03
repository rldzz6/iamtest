from io import StringIO
from iamtest.models.entity import group
from iamtest.commons import util
import iamtest.commons.config as config

def select_group(data):
    db = config.db_connection()
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

        result = db.query(query, param=data, model=group.Group)
        db.connection.commit()
    except Exception as Err:
        print(Err)
        db.connection.rollback()
    return result

def insert_group(data):
    db = config.db_connection()
    try:
        insert_query  = util.make_insert_query('group', data)
        select_query = ' SELECT @@IDENTITY AS group_id; '

        db.execute(insert_query, param=data)
        result = db.query(select_query, param=data, model=group.Group)[0]

        db.connection.commit()
    except Exception as Err:
        db.connection.rollback()
        print(Err)
        print("**********SQL EXECUTE ERROR********")
    return result

def update_group(target_id, data):
    db = config.db_connection()
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
        
        result = db.execute(query, param=data)
        db.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        db.connection.rollback()
    return result

def delete_group(target_id):
    db = config.db_connection()
    try:
        query = '''
            DELETE FROM `group` WHERE group_id = ?group_id?;
        '''
        #TODO : 권한그룹에 할당된 권한 삭제
        
        result = db.execute(query, param={'group_id': target_id})
        db.connection.commit()
    except Exception as Err:
        print("**********SQL EXECUTE ERROR********")
        print(Err)
        db.connection.rollback()
    return result