
import unittest

from test.models.test_models import TestDeptModel
from test.utils.test_query_string import TestQueryString
from test.biz.test_dept import TestDeptBiz
from test.biz.test_emp import TestEmptBiz
from test.api.test_dept import TestDeptApi
from test.api.test_emp import TestEmpApi

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest( unittest.makeSuite(TestDeptModel) )
    suite.addTest( unittest.makeSuite(TestQueryString) )
    suite.addTest(unittest.makeSuite(TestDeptBiz))
    suite.addTest(unittest.makeSuite(TestEmptBiz))
    suite.addTest(unittest.makeSuite(TestDeptApi))
    suite.addTest(unittest.makeSuite(TestEmpApi))
    return suite


if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)