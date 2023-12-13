from io import StringIO
from iamtest.commons import util
from iamtest.commons import config
from iamtest.models.entity import service

#서비스 목록 조회
def select_service(conn, data, page_no):
    try:
        query = f'''
            SELECT
                A.service_id
                , A.service_name
                , A.service_url
            FROM
                service A
            WHERE
                1 = 1
        ''' 
        if util.is_value('service_id', data) and data.service_id:
            query += " AND A.service_id = '{}' ".format(data.service_id)
        if util.is_value('keyword', data) and data.keyword:
            query += " AND (LOCATE('{keyword}', A.service_name) > 0  OR  LOCATE('{keyword}', A.service_url) > 0 ) ".format(keyword = data.keyword)
        query += util.pagination(page_no)        

        with conn.cursor() as cur:
            cur.execute(query)
            columns = cur.description
            result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cur.fetchall()]
            return result
    except Exception as error:
        raise Exception(error)

#서비스 전체 갯수 조회
def select_service_count(conn, data):
    try:
        query = f'''
            SELECT
                COUNT(*) AS count
            FROM
                service A
            WHERE
                1 = 1
        ''' 
        if util.is_value('service_id', data) and data.service_id:
            query += " AND A.service_id = '{}' ".format(data.service_id)
        if util.is_value('keyword', data) and data.keyword:
            query += " AND (LOCATE('{keyword}', A.service_name) > 0  OR  LOCATE('{keyword}', A.service_url) > 0 ) ".format(keyword = data.keyword)

        with conn.cursor() as cur:
            cur.execute(query)
            result=cur.fetchone()
            return result
    except Exception as error:
        raise Exception(error)

#서비스 생성
def insert_service(conn, data):
    try:
        query = util.make_insert_query('service', data)

        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            return cur.lastrowid
    except Exception as error:
        conn.rollback()
        raise Exception(error)

#서비스 정보 수정
def update_service(conn, target_id, data):
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                service
            SET 
                {update_values}
            WHERE
                service_id = {target_id};
        '''

        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except Exception as error:
        conn.rollback()
        raise Exception(error)

#서비스 삭제
def delete_service(conn, target_id):
    try:
        query = f'''
            DELETE FROM service WHERE service_id = '{target_id}';
        '''
        #TODO : 서비스 하위 리소스 및 권한 삭제

        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except Exception as error:
        conn.rollback()
        raise Exception(error)