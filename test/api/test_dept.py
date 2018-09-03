

import unittest
from app import *
from app.utils import *
from app.config import config



class TestDeptApi(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDeptApi, self).__init__(*args, **kwargs)



    def setUp(self):
        self.app = create_app(config['test']).test_client()



    def test_search_dept(self):
        response = self.app.get("/api/dept/search")
        res_json = response.json
        self.assertTrue(res_json.get('status') == 200)
        self.assertTrue(res_json.get('count') > 0)


    def test_add_dept(self):
        new_dept = {
            'deptno': 50,
            'dname': '연구소',
            'loc': '서울 강남'
        }
        response = self.app.post('/api/dept', json=new_dept)
        res_json = response.json
        logger.debug(res_json)
        self.assertTrue(res_json.get('status') == 200)
        self.assertTrue(res_json.get('count') > 0)


    def test_add_dept_require_deptno(self):
        new_dept = {
            # 'deptno': 50,
            'dname': '연구소',
            'loc': '서울 강남'
        }
        response = self.app.post('/api/dept', json=new_dept)
        res_json = response.json
        logger.debug(res_json)
        self.assertTrue(res_json.get('status') == 400)
        self.assertTrue(res_json.get('messages')[0].find('Required field') > -1)


    def test_add_dept_require_dname(self):
        new_dept = {
            'deptno': 50,
            # 'dname': '연구소',
            'loc': '서울 강남'
        }
        response = self.app.post('/api/dept', json=new_dept)
        res_json = response.json
        logger.debug(res_json)
        self.assertTrue(res_json.get('status') == 400)
        self.assertTrue(res_json.get('messages')[0].find('Required field') > -1)


    def test_add_dept_valid_multi(self):
        new_dept = {
            'deptno': 50,
            # 'dname': '연구소',
            # 'loc': '서울 강남'
        }
        response = self.app.post('/api/dept', json=new_dept)
        res_json = response.json
        self.assertTrue(res_json.get('status') == 400)
        self.assertTrue( len(res_json.get('messages')) == 2)


    def test_del_dept(self):
        new_dept = {
            'deptno': 90,
            'dname': '연구소',
            'loc': '서울 강남'
        }
        response = self.app.post('/api/dept', json=new_dept)
        res_json = response.json
        self.assertTrue(res_json.get('status') == 200)
        self.assertTrue(res_json.get('count') > 0)

        response = self.app.delete('/api/dept/90')
        res_json = response.json
        self.assertTrue(res_json.get('status') == 200)

        response = self.app.get("/api/dept/90")
        res_json = response.json
        logger.debug(res_json)
        self.assertTrue(res_json.get('status') == 404)