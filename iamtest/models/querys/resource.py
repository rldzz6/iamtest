from io import StringIO
from iamtest.commons import util
from iamtest.commons import config
from iamtest.models.entity import resource

#리소스 목록 조회
def select_resource(conn, data, page_no):
    try:
        query = f'''
            SELECT
                A.resource_id
                , A.resource_name
                , A.remark
                , B.service_id
                , B.service_name
            FROM
                resource A
                JOIN service B ON A.service_id = B.service_id
            WHERE
                1 = 1
        '''
        if util.is_value('resource_id', data) and data.resource_id:
            query += " AND A.resource_id = '{}'".format(data.resource_id)
        if util.is_value('service_id', data) and data.service_id:
            query += " AND A.service_id = '{}'".format(data.service_id)
        if util.is_value('resource_name', data) and data.resource_name:
            query += " AND A.resource_name = '{}'".format(data.resource_name)
        if util.is_value('keyword', data) and data.keyword:
            query += " AND (LOCATE('{keyword}', A.resource_name) > 0  OR  LOCATE('{keyword}', A.remark) > 0 ) ".format(keyword = data.keyword)
        query += util.pagination(page_no)

        with conn.cursor() as cur:
            cur.execute(query)
            columns = cur.description
            result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cur.fetchall()]
            return result
    except Exception as error:
        raise Exception(error)

#리소스 전체 갯수 조회
def select_resource_count(conn, data):
    try:
        query = f'''
            SELECT
                COUNT(*) AS count
            FROM
                resource A
                JOIN service B ON A.service_id = B.service_id
            WHERE
                1 = 1
        '''
        if util.is_value('resource_id', data) and data.resource_id:
            query += " AND A.resource_id = '{}'".format(data.resource_id)
        if util.is_value('service_id', data) and data.service_id:
            query += " AND A.service_id = '{}'".format(data.service_id)
        if util.is_value('resource_name', data) and data.resource_name:
            query += " AND A.resource_name = '{}'".format(data.resource_name)
        if util.is_value('keyword', data) and data.keyword:
            query += " AND (LOCATE('{keyword}', A.resource_name) > 0  OR  LOCATE('{keyword}', A.remark) > 0 ) ".format(keyword = data.keyword)

        with conn.cursor() as cur:
            cur.execute(query)
            result=cur.fetchone()
            return result
    except Exception as error:
        raise Exception(error)

#리소스 생성
def insert_resource(conn, data):
    try:
        query = util.make_insert_query('resource', data)

        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            return cur.lastrowid
    except Exception as error:
        conn.rollback()
        raise Exception(error)

#리소스 정보 수정
def update_resource(conn, target_id, data):
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                resource
            SET 
                {update_values}
            WHERE
                resource_id = {target_id};
        '''

        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except Exception as error:
        conn.rollback()
        raise Exception(error)

#리소스 삭제
def delete_resource(conn, target_id):
    try:
        query = f'''
            DELETE FROM resource WHERE resource_id = '{target_id}';
        '''
        #TODO : 리소스 하위 권한 삭제
        
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except Exception as error:
        conn.rollback()
        raise Exception(error)