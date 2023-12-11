from io import StringIO
from iamtest.commons import util
from iamtest.commons import config
from iamtest.models.entity import permission

#권한 정보 조회
def select_permission(data, page_no):
    db = config.db_connection()
    search_option = util.make_search_option(data, ['permission_name', 'remark'])
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
            WHERE
                1 = 1
        ''' 
        query += search_option
        query += util.pagination(page_no) 

        if search_option != '':
            result = db.query(query, param=data, model=permission.Permission)
        else:
            result = db.query(query, model=permission.Permission)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한 전체 갯수 조회
def select_permission_count(data):
    db = config.db_connection()
    search_option = util.make_search_option(data, ['permission_name', 'remark'])
    try:
        query = f'''
            SELECT
                COUNT(*) AS count
            FROM
                permission
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

def select_user(data, page_no):
    db = config.db_connection()
    try:
        query = f'''
            SELECT
                A.employee_id
                , B.employee_name
                , C.permission_id
                , C.permission_name
                , C.permission
                , D.group_id AS group_id
                , E.group_name AS group_name
            FROM
                user_permission A
                JOIN employee B ON A.employee_id = B.id
                LEFT JOIN group_permission D ON A.group_id = D.group_id
                LEFT JOIN `group` E ON D.group_id = E.group_id
                JOIN permission C ON C.permission_id = D.permission_id OR A.permission_id = C.permission_id
            WHERE
                1 = 1
        '''
        if data.permission_id:
            query += ' AND (A.permission_id = ?permission_id? OR C.permission_id = ?permission_id?) '
        if data.keyword:
            query += ' AND (B.employee_name = ?keyword? OR E.group_name = ?keyword?) '
        if data.employee_id:
            query += ' AND (A.employee_id = ?employee_id?) '

        result = db.execute_scalar(query, param=data)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

def select_user_count(data):
    db = config.db_connection()
    search_option = util.make_search_option(data, ['permission_name', 'remark'])
    try:
        query = f'''
            SELECT
                COUNT(*) AS count
            FROM
                user_permission A
                JOIN employee B ON A.employee_id = B.id
                LEFT JOIN group_permission D ON A.group_id = D.group_id
                LEFT JOIN `group` E ON D.group_id = E.group_id
                JOIN permission C ON C.permission_id = D.permission_id OR A.permission_id = C.permission_id
            WHERE
                1 = 1
        '''
        if data.permission_id:
            query += ' AND (A.permission_id = ?permission_id? OR C.permission_id = ?permission_id?) '
        if data.keyword:
            query += ' AND (B.employee_name = ?keyword? OR E.group_name = ?keyword?) '
        if data.employee_id:
            query += ' AND (A.employee_id = ?employee_id?) '
        
        if search_option != '':
            result = db.execute_scalar(query, param=data)
        else:
            result = db.execute_scalar(query)
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한 생성
def insert_permission(data):
    db = config.db_connection()
    try:
        insert_query = util.make_insert_query('permission', data)
        select_query = 'SELECT @@IDENTITY AS permission_id;'

        db.execute(insert_query, param=data)
        result = db.query_single(select_query, model=permission.Permission)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한 정보 수정
def update_permission(target_id, data):
    db = config.db_connection()
    
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                permission
            SET 
                {update_values}
            WHERE
                permission_id = {target_id};
        '''

        result = db.execute(query, param=data)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#권한 삭제
def delete_permission(target_id):
    db = config.db_connection()
    try:
        query = '''
            DELETE FROM permission WHERE permission_id = ?permission_id?;
        '''
        #TODO : 할당되어있는 권한정보 삭제(user_permission, group_permission)
        
        result = db.execute(query, param={'permission_id': target_id})

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#사원에게 권한 할당 (권한 또는 권한그룹)
def allocation_permission(data):
    db = config.db_connection()
    try:
        query = util.make_insert_query('user_permission', data)

        db.execute(query, param=data)
        db.connection.commit()
        return
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

#사원에게 할당된 권한그룹 제거
def clear_permission(group_id, emplyoee_id):
    db = config.db_connection()
    try:
        query = '''
            DELETE FROM user_permission WHERE group_id = ?group_id?
        '''
        if emplyoee_id:
            query += ' AND employee_id = ?emplyoee_id?'

        print(query)
        db.execute(query, param={'group_id':group_id, 'emplyoee_id':emplyoee_id})
        db.connection.commit()
        return
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)