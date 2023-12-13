from io import StringIO
from iamtest.commons import util
from iamtest.commons import config
import iamtest.models.entity.permission as Entity

#권한 정보 조회
def select_permission(conn, data, page_no):
    try:
        query = f'''
            SELECT
                A.permission_id
                , A.permission_name
                , A.permission
                , A.remark
                , B.resource_id
                , B.resource_name
				, C.service_id
                , C.service_name
            FROM
                permission A
                JOIN resource B ON A.resource_id = B.resource_id
                JOIN service C ON A.service_id = C.service_id
            WHERE
                1 = 1
        ''' 
        if util.is_value('permission_id', data) and data.permission_id:
            query += " AND A.permission_id = '{}' ".format(data.permission_id)
        if util.is_value('service_id', data) and data.service_id:
            query += " AND A.service_id = '{}' ".format(data.service_id)
        if util.is_value('resource_id', data) and data.resource_id:
            query += " AND A.resource_id = '{}' ".format(data.resource_id)
        if util.is_value('permission_name', data) and data.permission_name:
            query += " AND A.permission_name = '{}' ".format(data.permission_name)
        if util.is_value('keyword', data) and data.keyword:
            query += " AND (LOCATE('{keyword}', A.permission_name) > 0  OR  LOCATE('{keyword}', A.remark) > 0 ) ".format(keyword = data.keyword)
        query += util.pagination(page_no) 

        with conn.cursor() as cur:
            cur.execute(query)
            result = [Entity.Model(permission=data).permission for data in cur.fetchall()]
            return result
    except Exception as error:
        raise Exception(error)

#권한 전체 갯수 조회
def select_permission_count(conn, data):
    try:
        query = f'''
            SELECT
                COUNT(*) AS count
            FROM
                permission A
                JOIN resource B ON A.resource_id = B.resource_id
                JOIN service C ON A.service_id = C.service_id
            WHERE
                1 = 1
        ''' 
        if util.is_value('permission_id', data) and data.permission_id:
            query += " AND A.permission_id = '{}' ".format(data.permission_id)
        if util.is_value('service_id', data) and data.service_id:
            query += " AND A.service_id = '{}' ".format(data.service_id)
        if util.is_value('resource_id', data) and data.resource_id:
            query += " AND A.resource_id = '{}' ".format(data.resource_id)
        if util.is_value('permission_name', data) and data.permission_name:
            query += " AND A.permission_name = '{}' ".format(data.permission_name)
        if util.is_value('keyword', data) and data.keyword:
            query += " AND (LOCATE('{keyword}', A.permission_name) > 0  OR  LOCATE('{keyword}', A.remark) > 0 ) ".format(keyword = data.keyword)

        with conn.cursor() as cur:
            cur.execute(query)
            result=cur.fetchone()
            return result[0]
    except Exception as error:
        raise Exception(error)

#권한 생성
def insert_permission(conn, data):
    try:
        query = util.make_insert_query('permission', data)

        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            return cur.lastrowid
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 : ' + str(error))

#권한 정보 수정
def update_permission(conn, target_id, data):
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                permission
            SET 
                {update_values}
            WHERE
                permission_id = '{target_id}';
        '''
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            return cur.rowcount
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 : ' + str(error))

#권한 삭제
def delete_permission(conn, permission_id):
    try:
        #할당되어있는 권한정보도 모두 삭제(permission, user_permission, group_permission)
        query_user_permission = f"DELETE FROM group_permission WHERE permission_id = '{permission_id}'";
        query_group_permission = f"DELETE FROM user_permission WHERE permission_id = '{permission_id}';"
        quesry_permission = f"DELETE FROM permission WHERE permission_id = '{permission_id}';"


        with conn.cursor() as cur:
            cur.execute(query_user_permission)
            cur.execute(query_group_permission)
            cur.execute(quesry_permission)
            conn.commit()
            return cur.rowcount
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 : ' + str(error))

def select_user(conn, data, page_no = 0):
    try:
        query = f'''
           SELECT DISTINCT
                A.employee_id
                , B.employee_name
                , C.permission_id
                , C.permission_name
                , C.permission
                , D.group_id AS group_id
                , E.group_name AS group_name
                , CASE WHEN NULLIF(A.group_id, '') <> '' THEN 'G' ELSE 'P' END AS permission_type
                , F.resource_id
                , F.resource_name
                , G.service_id
                , G.service_name
            FROM
                user_permission A
                JOIN employee B ON A.employee_id = B.employee_id
                LEFT JOIN group_permission D ON A.group_id = D.group_id
                LEFT JOIN `group` E ON D.group_id = E.group_id
                JOIN permission C ON C.permission_id = D.permission_id OR A.permission_id = C.permission_id
                JOIN resource F ON C.resource_id = F.resource_id
                JOIN service G ON C.service_id = G.service_id
            WHERE
                1 = 1
        '''
        if util.is_value('permission_id', data) and data.permission_id:
            query += " AND (A.permission_id = '{permission_id}' OR C.permission_id = '{permission_id}') ".format(permission_id = data.permission_id)
        if util.is_value('keyword', data) and data.keyword:
            query += " AND (B.employee_name = '{keyword}' OR E.group_name = '{keyword}') ".format(keyword = data.keyword)
        if util.is_value('employee_id', data) and data.employee_id:
            query += " AND (A.employee_id = '{employee_id}') ".format(employee_id = data.employee_id)
        query += util.pagination(page_no)     
                
        with conn.cursor() as cur:
            cur.execute(query)
            result = [Entity.Model(user=data).user for data in cur.fetchall()]
            return result
    except Exception as error:
        raise Exception('쿼리 실행 오류(1) : ' + str(error))

def select_user_count(conn, data):
    try:
        query = f'''
            SELECT
                COUNT(*) AS count
            FROM
                user_permission A
                JOIN employee B ON A.employee_id = B.employee_id
                LEFT JOIN group_permission D ON A.group_id = D.group_id
                LEFT JOIN `group` E ON D.group_id = E.group_id
                JOIN permission C ON C.permission_id = D.permission_id OR A.permission_id = C.permission_id
                JOIN resource F ON C.resource_id = F.resource_id
                JOIN service G ON C.service_id = G.service_id
            WHERE
                1 = 1
        '''
        if util.is_value('permission_id', data) and data.permission_id:
            query += " AND (A.permission_id = '{permission_id}' OR C.permission_id = '{permission_id}') ".format(permission_id = data.permission_id)
        if util.is_value('keyword', data) and data.keyword:
            query += " AND (B.employee_name = '{keyword}' OR E.group_name = '{keyword}') ".format(keyword = data.keyword)
        if util.is_value('employee_id', data) and data.employee_id:
            query += " AND (A.employee_id = '{employee_id}') ".format(employee_id = data.employee_id)

        with conn.cursor() as cur:
            cur.execute(query)
            result=cur.fetchone()
            return result[0]
    except Exception as error:
        raise Exception('쿼리 실행 오류(2) : ' + str(error))

#사원에게 권한 할당 (권한 또는 권한그룹)
def allocation_user_permission(conn, data):
    try:
        #query = util.make_insert_query('user_permission', data)
        query = "INSERT INTO user_permission (employee_id, permission_id, group_id) VALUES (%s, %s, %s) "

        with conn.cursor() as cur:
            cur.executemany(query, data)
            conn.commit()
            print(cur.rowcount)
            return cur.rowcount
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 (allocation_user_permission) : ' + str(error))

#사원에게 할당된 권한 또는 권한그룹 제거
def clear_user_permission(conn, data):
    try:
        query = '''
            DELETE FROM user_permission WHERE employee_id = %s
            AND (NULLIF(permission_id, '') <> '' AND NULLIF(permission_id, '') = %s AND (NULLIF(group_id, '') <> '' AND NULLIF(group_id, '') = %s))
        '''

        with conn.cursor() as cur:
            cur.executemany(query, data)
            conn.commit()
            print(cur.rowcount)
            return cur.rowcount
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 (clear_user_permission) : ' + str(error))