import unittest

from app.biz.emp import EmployeeBiz

from app.errors import ContentsNotFoundException
from app import *
from app.config import config

class TestEmptBiz(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config['test'])
        self.app_context = self.app.app_context()
        self.app_context.push()



    def tearDown(self):
        db.session.remove()
        self.app_context.pop()



    def test_search_emp(self):
        biz = EmployeeBiz()
        rows = biz.get_emp_list(size=10)
        self.assertTrue(len(rows) == 10)


    def test_search_king_emp(self):
        biz = EmployeeBiz()
        rows = biz.get_emp_list(ename='KING')
        self.assertTrue(len(rows) == 1)
        self.assertTrue(rows[0].get('ename') == 'KING')


    def test_add_emp(self):
        biz = EmployeeBiz()
        new_emp = {
            "empno": 8000,
            "ename": "NEWWMP",
            "job": "ANALYST",
            "mgr": 7782,
            "hiredate": "1982-11-09",
            "sal": 5000,
            "comm": None,
            "deptno": 20
        }
        biz.add_emp(new_emp)
        emp = biz.get_emp(8000)
        self.assertTrue(emp.get('ename') == 'NEWWMP')


    def test_update_emp(self):
        biz = EmployeeBiz()
        new_emp = {
            "empno": 8001,
            "ename": "NEWWMP",
            "job": "ANALYST",
            "mgr": 7782,
            "hiredate": "1982-11-09",
            "sal": 5000,
            "comm": None,
            "deptno": 20
        }
        biz.add_emp(new_emp)
        new_emp = {
            "empno": 8001,
            "ename": "RENAME",
            "job": "CLERK",
            "mgr": 7782,
            "hiredate": "1999-12-31",
            "sal": 4300,
            "comm": 1200,
            "deptno": 10
        }
        biz.add_emp(new_emp)

        emp = biz.get_emp(8001)
        self.assertTrue(emp.get('ename') == 'RENAME')
        self.assertTrue(emp.get('job') == 'CLERK')
        self.assertTrue(emp.get('sal') == 4300.00)
        self.assertTrue(emp.get('comm') == 1200.00)
        self.assertTrue(emp.get('hiredate') == '1999-12-31')
        self.assertTrue(emp.get('dept').get('deptno') == 10)



    def test_del_emp(self):
        biz = EmployeeBiz()
        new_emp = {
            "empno": 8002,
            "ename": "NEWWMP",
            "job": "ANALYST",
            "mgr": 7782,
            "hiredate": "1982-11-09",
            "sal": 5000,
            "comm": None,
            "deptno": 20
        }
        biz.add_emp(new_emp)
        emp = biz.del_emp(8002)
        self.assertRaises(ContentsNotFoundException, lambda : biz.get_emp(8002))