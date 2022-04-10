import json
import logging
import pymysql
import requests
from bs4 import BeautifulSoup
import app
# 封装断言
# 断言时有响应状态码status_code，响应码status以及描述信息description
def assert_utils(self,response,status_code,status,desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))
# 获取第三方的接口数据
def request_third_api(form_data):
    # 解析form表单中的内容，并提取第三方请求的参数
    soup = BeautifulSoup(form_data, "html.parser")
    third_url = soup.form['action']
    logging.info("third request url = {}".format(third_url))
    data = {}
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value'])
    logging.info("third request data = {}".format(data))
    # 发送第三方请求
    response = requests.post(third_url, data=data)
    return response

# 连接数据库，进行自动化的数据清除操作
class DButils:
    @classmethod
    def get_conn(cls,db_name):
        conn = pymysql.connect(app.DB_URL,app.DB_USERNAME,app.DB_PASSWORD,db_name,autocommit=True)
        return  conn
    @classmethod
    def close(cls,cursor = None,conn = None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    @classmethod
    def delete(cls,db_name,sql):
        try:
            conn=cls.get_conn(db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close(cursor,conn)
# 读取参数化的数据包
def read_imgVerify_data(file_name):
    file = app.BASE_DIRB+"/data/"+file_name
    test_case_data=[]
    with open(file,encoding="utf-8") as f:
        verify_data = json.load(f)
        test_data_list = verify_data.get("test_get_img_verify_code")
        for test_data in test_data_list:
            test_case_data.append((test_data.get("type"),test_data.get("status_code")))
    print("json_data = {}".format(test_case_data))
    return test_case_data