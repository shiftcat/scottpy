
import unittest

from app.models.dept_model import Dept

class TestDeptModel(unittest.TestCase):

    def test_new_dept(self):
        dept = Dept()
        dept.deptno = 8900
        dept.dname = "연구소"
        dept.loc = "서울 중구"

        dept_dict = {
            'deptno': 8900,
            'dname': '연구소',
            'loc': '서울 중구'
        }

        self.assertDictEqual(dept.to_json(), dept_dict)