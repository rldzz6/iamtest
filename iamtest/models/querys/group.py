from io import StringIO
from iamtest.commons import util
import iamtest.commons.config as config
from iamtest.models.entity import group

def select_group(data):
    db = config.db_connection()
    
    search_option = util.make_search_option(data, ['group_name', 'remark'])
    try:
        query = f'''
            SELECT
                group_id
                , group_name
                , remark
            FROM
                `group`
            WHERE
                1 = 1
        ''' 
        query += search_option + ';'

        if search_option != '':
            result = db.query(query, param=data, model=group.Group)
        else:
            result = db.query(query, model=group.Group)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한그룹에 속한 사원 조회
def select_group_user(target_id):
    db = config.db_connection()
    try:
        query = f'''
            SELECT
                GROUP_CONCAT(DISTINCT employee_id) AS employee_list
            FROM
                user_permission A 
                JOIN `group` B ON A.group_id = B.group_id
            WHERE
                A.group_id = '{target_id}';
        '''

        result = db.query(query, model=group.Group_Permission)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한그룹의 권한 조회
def select_group_permission(target_id, data):
    db = config.db_connection()
    try:
        query = f'''
            SELECT DISTINCT
                row_number() over (order by B.service_id, B.resource_id, B.permission_id) AS no
                , A.group_id
                , C.service_id
                , C.service_name
                , D.resource_id
                , D.resource_name
                , B.permission_id
                , B.permission_name
                , B.permission
            FROM
                group_permission A
                JOIN permission B ON A.permission_id = B.permission_id
                JOIN service C ON B.service_id = C.service_id
                JOIN resource D ON B.resource_id = D.resource_id
            WHERE
                A.group_id = '{target_id}'
        '''
        if data.service_id:
            query += ' AND C.service_id = ?service_id? '
        if data.resource_id:
            query += ' AND D.resource_id = ?resource_id? '
        if data.permission_name:
            query += ' AND LOCATE(?permission_name?, B.permission_name) > 0 '
        query += 'GROUP BY A.group_id, C.service_id, C.service_name, D.resource_id, D.resource_name, B.permission_id, B.permission_name, B.permission;'

        if data:
            result = db.query(query, param=data, model=group.Group_Permission)
        else:
            result = db.query(query, model=group.Group_Permission)
        print(result)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

def insert_group(data):
    db = config.db_connection()
    try:
        insert_query = util.make_insert_query('group', data)
        select_query = 'SELECT @@IDENTITY AS group_id;'

        db.execute(insert_query, param=data)
        result = db.query_first(select_query, model=group.Group)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

def update_group(target_id, data):
    db = config.db_connection()
    
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                `group`
            SET 
                {update_values}
            WHERE
                group_id = {target_id};
        '''

        result = db.execute(query, param=data)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

def delete_group(target_id):
    db = config.db_connection()
    try:
        query = '''
            DELETE FROM `group` WHERE group_id = ?group_id?;
        '''

        result = db.execute(query, param={'group_id': target_id})

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)