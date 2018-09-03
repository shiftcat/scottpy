
import unittest
from app import create_app, logger
from app.config import config


class TestEmpApi(unittest.TestCase):


    def setUp(self):
        self.app = create_app(config['test']).test_client()


    def test_search_emp(self):
        response = self.app.get("/api/emp/search")
        res_json = response.json
        self.assertTrue(res_json.get('status') == 200)
        self.assertTrue(res_json.get('count') > 0)


    def test_search_emp_size(self):
        response = self.app.get("/api/emp/search", query_string={'size': 5})
        res_json = response.json
        self.assertTrue(res_json.get('status') == 200)
        self.assertTrue(res_json.get('count') == 5)


    def test_search_emp_king(self):
        response = self.app.get("/api/emp/search", query_string={'ename': 'KING', 'deptno': 10})
        res_json = response.json
        self.assertTrue(res_json.get('status') == 200)
        self.assertTrue(res_json.get('result')[0].get('ename') == 'KING')


    def test_add_emp(self):
        new_emp = {
            "empno": 9001,
            "ename": "NEWWMP",
            "job": "ANALYST",
            "mgr": 7782,
            "hiredate": "1982-11-09",
            "sal": 5000,
            "comm": None,
            "deptno": 20
        }

        response = self.app.post('/api/emp', json=new_emp)
        res_json = response.json
        logger.debug(res_json)
        self.assertTrue(res_json.get('status') == 200)
        self.assertTrue(res_json.get('count') > 0)


    def test_require_empno(self):
        new_emp = {
            # "empno": 8900,
            "ename": "NEWWMP",
            "job": "ANALYST",
            "mgr": 7782,
            "hiredate": "1982-11-09",
            "sal": 5000,
            "comm": None,
            "deptno": 20
        }

        response = self.app.post('/api/emp', json=new_emp)
        res_json = response.json
        logger.debug(res_json)
        self.assertTrue(res_json.get('status') == 400)
        self.assertTrue(res_json.get('messages')[0].find('Required field') > -1)


    def test_require_hiredate(self):
        new_emp = {
            "empno": 8900,
            "ename": "NEWWMP",
            "job": "ANALYST",
            "mgr": 7782,
            # "hiredate": "1982-11-09",
            "sal": 5000,
            "comm": None,
            "deptno": 20
        }

        response = self.app.post('/api/emp', json=new_emp)
        res_json = response.json
        logger.debug(res_json)
        self.assertTrue(res_json.get('status') == 400)
        self.assertTrue(res_json.get('messages')[0].find('Required field') > -1)


    def test_hiredate_format(self):
        new_emp = {
            "empno": 8900,
            "ename": "NEWWMP",
            "job": "ANALYST",
            "mgr": 7782,
            "hiredate": "1982-11-99",
            "sal": 5000,
            "comm": None,
            "deptno": 20
        }

        response = self.app.post('/api/emp', json=new_emp)
        res_json = response.json
        logger.debug(res_json)
        self.assertTrue(res_json.get('status') == 400)
        self.assertTrue(res_json.get('messages')[0].find("'date' format") > -1)



    def test_del_emp(self):
        new_emp = {
            "empno": 9002,
            "ename": "NEWWMP",
            "job": "ANALYST",
            "mgr": 7782,
            "hiredate": "1982-11-09",
            "sal": 5000,
            "comm": None,
            "deptno": 20
        }

        response = self.app.post('/api/emp', json=new_emp)
        res_json = response.json
        logger.debug(res_json)
        self.assertTrue(res_json.get('status') == 200)
        self.assertTrue(res_json.get('count') > 0)

        response = self.app.delete('/api/emp/9002')
        res_json = response.json
        logger.debug(res_json)
        self.assertTrue(res_json.get('status') == 200)

        response = self.app.get("/api/emp/9002")
        res_json = response.json
        logger.debug(res_json)
        self.assertTrue(res_json.get('status') == 404)