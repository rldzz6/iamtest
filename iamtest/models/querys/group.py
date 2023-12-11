from io import StringIO
from iamtest.commons import util
from iamtest.commons import config
from iamtest.models.entity import group

def select_group(data, page_no=1):

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
        query += search_option
        query += util.pagination(page_no)

        if search_option != '':
            result = db.query(query, param=data, model=group.Group)
        else:
            result = db.query(query, model=group.Group)
        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한그룹 전체 갯수 조회
def select_group_count(data):
    db = config.db_connection()
    search_option = util.make_search_option(data, ['group_name', 'remark'])
    try:
        query = f'''
            SELECT
                COUNT(*) AS count
            FROM
                `group`
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

#권한그룹에 속한 사원 조회
def select_group_user(target_id):
    db = config.db_connection()
    try:
        query = f'''
            SELECT DISTINCT
                B.group_id
                , A.employee_id
                , C.employee_name
            FROM
                user_permission A 
                JOIN `group` B ON A.group_id = B.group_id
                JOIN employee C ON A.employee_id = C.id
            WHERE
                A.group_id = '{target_id}';
        '''

        result = db.query(query, model=group.Permission)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한그룹의 권한 조회
def select_group_permission(data, page_no = 1):
    db = config.db_connection()
    try:
        query = f'''
            SELECT DISTINCT
                A.group_id
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
                JOIN `resource` D ON B.resource_id = D.resource_id
            WHERE
                A.group_id = ?group_id?
        '''
        if util.is_value('service_id', data) and data.service_id:
            query += ' AND C.service_id = ?service_id? '
        if util.is_value('resource_id', data) and data.resource_id:
            query += ' AND D.resource_id = ?resource_id? '
        if util.is_value('permission_name', data) and data.permission_name:
            query += ' AND LOCATE(?permission_name?, B.permission_name) > 0 '
        query += ' GROUP BY A.group_id, C.service_id, C.service_name, D.resource_id, D.resource_name, B.permission_id, B.permission_name, B.permission '
        query += util.pagination(page_no)

        if data:
            result = db.query(query, param=data, model=group.Permission)
        else:
            result = db.query(query, model=group.Permission)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한그룹의 권한 갯수 조회
def select_group_permission_count(target_id, data):
    db = config.db_connection()
    try:
        query = f'''
            SELECT DISTINCT
                COUNT(*) AS count
            FROM
                group_permission A
                JOIN permission B ON A.permission_id = B.permission_id
                JOIN service C ON B.service_id = C.service_id
                JOIN `resource` D ON B.resource_id = D.resource_id
            WHERE
                A.group_id = ?group_id?
        '''
        if data.service_id:
            query += ' AND C.service_id = ?service_id? '
        if data.resource_id:
            query += ' AND D.resource_id = ?resource_id? '
        if data.permission_name:
            query += ' AND LOCATE(?permission_name?, B.permission_name) > 0 '
        query += 'GROUP BY A.group_id, C.service_id, C.service_name, D.resource_id, D.resource_name, B.permission_id, B.permission_name, B.permission'

        if data:
            result = db.execute_scalar(query, param=data)
        else:
            result = db.execute_scalar(query)
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한그룹 생성
def insert_group(data):
    db = config.db_connection()
    try:
        insert_query = util.make_insert_query('group', data)
        select_query = 'SELECT @@IDENTITY AS group_id;'

        db.execute(insert_query, param=data)
        result = db.query_single(select_query, model=group.Group)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한그룹 정보 업데이트
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

#권한그룹 삭제
def delete_group(target_id):
    db = config.db_connection()
    try:
        query = '''
            DELETE FROM `group` WHERE group_id = ?group_id?;
        '''
        #TODO : 권한그룹에 할당된 권한삭제
        result = db.execute(query, param={'group_id': target_id})

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한그룹에 권한 할당
def allocation_permission(data):
    db = config.db_connection()
    try:
        query = util.make_insert_query('group_permission', data)

        db.execute(query, param=data)
        db.connection.commit()
        return
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한그룹에 할단된 권한 제거
def clear_permission(group_id, permission_id):
    db = config.db_connection()
    try:
        query = '''
            DELETE FROM group_permission WHERE group_id = ?group_id?
        '''
        if permission_id:
            query += ' AND permission_id = ?permission_id?'

        print(query)
        db.execute(query, param={'group_id':group_id, 'permission_id':permission_id})
        db.connection.commit()
        return
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

