
import unittest

from app.biz.dept import DepartmentBiz

from app.errors import ContentsNotFoundException
from app import *

from app.config import config

class TestDeptBiz(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config['test'])
        self.app_context = self.app.app_context()
        self.app_context.push()



    def tearDown(self):
        db.session.remove()
        self.app_context.pop()



    def test_search_dept(self):
        biz = DepartmentBiz()
        rows = biz.get_dept_list()
        self.assertTrue(len(rows) > 0, "부서목록 조회결과 없습니다.")


    def test_get_dept(self):
        biz = DepartmentBiz()
        dept = biz.get_dept(10)
        self.assertTrue(dept.get('deptno') == 10, "부서번호 10번이 아닌 부서 입니다.")


    def test_add_dept(self):
        biz = DepartmentBiz()
        try:
            biz.del_dpet(50)
        except:
            pass
        new_dept = {
            'deptno': 50,
            'dname': '연구소',
            'loc': '서울 강남'
        }
        biz.add_dept(new_dept)

        dept = biz.get_dept(50)
        self.assertTrue(dept.get('deptno') == 50, "부서번호 50번이 아닌 부서 입니다.")
        self.assertTrue(dept.get('dname') == '연구소', "50번 부서는 연구소 부서가 아님니다.")
        self.assertTrue(dept.get('loc') == '서울 강남', "50번 부서의 위치는 서울 강남 아님니다.")


    def test_del_dept(self):
        biz = DepartmentBiz()
        new_dept = {
            'deptno': 60,
            'dname': '연구소',
            'loc': '서울 강남'
        }
        biz.add_dept(new_dept)

        biz.del_dpet(60)
        self.assertRaises(ContentsNotFoundException, lambda : biz.get_dept(60))

