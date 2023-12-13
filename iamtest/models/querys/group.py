from io import StringIO
from iamtest.commons import util
from iamtest.commons import config
from iamtest.models.entity import group
import iamtest.models.entity.group as Entity

def select_group(conn, data, page_no):
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
        if util.is_value('group_id', data) and data.group_id:
            query += " AND group_id = {group_id} ".format(group_id=data.group_id)
        if util.is_value('keyword', data) and data.keyword:
            query += " AND (LOCATE('{keyword}', group_name) > 0  OR  LOCATE('{keyword}', remark) > 0 ) ".format(keyword = data.keyword)
        query += util.pagination(page_no)

        with conn.cursor() as cur:
            cur.execute(query)
            result = [Entity.Model(group=data).group for data in cur.fetchall()]
            return result
    except Exception as error:
        raise Exception('쿼리 실행 오류(1) : ' + str(error))

#권한그룹 전체 갯수 조회
def select_group_count(conn, data):
    try:
        query = f'''
            SELECT
                COUNT(*) AS count
            FROM
                `group`
            WHERE
                1 = 1
        ''' 
        if util.is_value('group_id', data) and data.group_id:
            query += " AND group_id = {} ".format(data.group_id)
        if util.is_value('keyword', data) and data.keyword: 
            query += " AND (LOCATE('{keyword}', group_name) > 0  OR  LOCATE('{keyword}', remark) > 0 ) ".format(keyword = data.keyword)

        with conn.cursor() as cur:
            cur.execute(query)
            result=cur.fetchone()
            return result[0]
    except Exception as error:
        raise Exception('쿼리 실행 오류(2) : ' + str(error))

#권한그룹에 속한 사원 조회
def select_group_user(conn, target_id):
    try:
        query = f'''
            SELECT DISTINCT
                B.group_id
                , A.employee_id
                , C.employee_name
                , C.employee_rank
            FROM
                user_permission A 
                JOIN `group` B ON A.group_id = B.group_id
                JOIN employee C ON A.employee_id = C.employee_id
            WHERE
                A.group_id = '{target_id}'
        '''

        with conn.cursor() as cur:
            cur.execute(query)
            result = [Entity.Model(permission=data).permission for data in cur.fetchall()]
            return result
    except Exception as error:
        raise Exception('쿼리 실행 오류 : ' + str(error))


#권한그룹의 권한 조회
def select_group_permission(conn, data, page_no=0):
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
                1=1
        '''
        if util.is_value('group_id', data) and data.group_id:
            query += " AND A.group_id = {}".format(data.group_id)
        if util.is_value('service_id', data) and data.service_id:
            query += " AND C.service_id = {}".format(data.service_id)
        if util.is_value('resource_id', data) and data.resource_id:
            query += " AND D.resource_id = {}".format(data.resource_id)
        if util.is_value('permission_name', data) and data.permission_name:
            query += " AND LOCATE('{permission_name}', B.permission_name) > 0 ".format(permission_name = data.permission_name)
        query += ' GROUP BY A.group_id, C.service_id, C.service_name, D.resource_id, D.resource_name, B.permission_id, B.permission_name, B.permission '
        query += util.pagination(page_no)

        with conn.cursor() as cur:
            cur.execute(query)
            result = [Entity.Model(permission=data).permission for data in cur.fetchall()]
            return result
    except Exception as error:
        raise Exception('쿼리 실행 오류 : ' + str(error))

#권한그룹의 권한 갯수 조회
def select_group_permission_count(conn, target_id, data):
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
                1=1
        '''
        if util.is_value('group_id', data) and data.group_id:
            query += " AND A.group_id = {}".format(data.group_id)
        if util.is_value('service_id', data) and data.service_id:
            query += " AND C.service_id = {}".format(data.service_id)
        if util.is_value('resource_id', data) and data.resource_id:
            query += " AND D.resource_id = {}".format(data.resource_id)
        if util.is_value('permission_name', data) and data.permission_name:
            query += " AND LOCATE('{permission_name}', B.permission_name) > 0 ".format(permission_name = data.permission_name)
        query += ' GROUP BY A.group_id, C.service_id, C.service_name, D.resource_id, D.resource_name, B.permission_id, B.permission_name, B.permission '

        with conn.cursor() as cur:
            cur.execute(query)
            result=cur.fetchone()
            return result[0]
    except Exception as error:
        raise Exception('쿼리 실행 오류 : ' + str(error))

#권한그룹 생성
def insert_group(conn, data):
    try:
        query = util.make_insert_query('group', data)

        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            return cur.lastrowid
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 : ' + str(error))

#권한그룹 정보 업데이트
def update_group(conn, group_id, data):
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                `group`
            SET 
                {update_values}
            WHERE
                group_id = '{group_id}';
        '''

        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            return cur.rowcount
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 : ' + str(error))

#권한그룹 삭제
def delete_group(conn, group_id):
    try:
        query_group = f"DELETE FROM `group` WHERE group_id = '{group_id}';"
        query_permission = f"DELETE FROM `group_permission` WHERE group_id = '{group_id}';"

        #TODO : 권한그룹에 할당된 권한삭제

        with conn.cursor() as cur:
            cur.execute(query_permission)
            cur.execute(query_group)
            conn.commit()
            return cur.rowcount
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 : ' + str(error))

#권한그룹에 권한 할당
def allocation_group_permission(conn, data):
    try:
        query = " INSERT INTO group_permission (group_id, permission_id) VALUES (%s, %s); "
        
        with conn.cursor() as cur:
            cur.executemany(query, data)
            conn.commit()
            print(cur.rowcount)
            return cur.rowcount
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 (allocation_group_permission) : ' + str(error))

#권한그룹에 할단된 권한 제거
def clear_group_permission(conn, data):
    try:
        query = '''
            DELETE FROM group_permission WHERE group_id = %s
            AND (NULLIF(permission_id, '') <> '' AND NULLIF(permission_id, '') = %s);
        '''

        with conn.cursor() as cur:
            cur.executemany(query, data)
            conn.commit()
            print(cur.rowcount)
            return cur.rowcount
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 (clear_group_permission) : ' + str(error))