from io import StringIO
from iamtest.commons import util
from iamtest.commons import config
import iamtest.models.entity.service as Entity

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
            query += " AND A.service_id = '{service_id}' ".format(service_id=data.service_id)
        if util.is_value('keyword', data) and data.keyword:
            query += " AND (LOCATE('{keyword}', A.service_name) > 0  OR  LOCATE('{keyword}', A.service_url) > 0 ) ".format(keyword = data.keyword)
        query += util.pagination(page_no)        

        with conn.cursor() as cur:
            cur.execute(query)
            result = [Entity.Model(data=data).data for data in cur.fetchall()]
            return result
    except Exception as error:
        raise Exception('쿼리 실행 오류(1) : ' + str(error))

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
        if data.service_id:
            query += " AND A.service_id = '{service_id}' ".format(service_id = data.service_id)
        if data.keyword:
            query += " AND (LOCATE('{keyword}', A.service_name) > 0  OR  LOCATE('{keyword}', A.service_url) > 0 ) ".format(keyword = data.keyword)

        with conn.cursor() as cur:
            cur.execute(query)
            result=cur.fetchone()
            return result[0]
    except Exception as error:
        raise Exception('쿼리 실행 오류(2) : ' + str(error))

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
        raise Exception('쿼리 실행 오류 : ' + str(error))

#서비스 정보 수정
def update_service(conn, service_id, data):
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                service
            SET 
                {update_values}
            WHERE
                service_id = '{service_id}';
        '''

        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            return cur.rowcount
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 : ' + str(error))

#서비스 삭제
def delete_service(conn, service_id):
    try:
        #서비스와 서비스에 등록된 리소스, 권핟도 일괄 삭제
        query_service = f"DELETE FROM service WHERE service_id = '{service_id}'";
        query_resource = f"DELETE FROM resource WHERE service_id = '{service_id}';"
        quesry_permission = f"DELETE FROM permission WHERE service_id = '{service_id}';"

        with conn.cursor() as cur:
            cur.execute(quesry_permission)
            cur.execute(query_resource)
            cur.execute(query_service)
            conn.commit()
            return cur.rowcount
    except Exception as error:
        conn.rollback()
        raise Exception('쿼리 실행 오류 : ' + str(error))