
import unittest

from app.utils.request import QueryString

class TestQueryString(unittest.TestCase):


    def test_init_query(self):
        query = "key1=value1&key2=한글값&key3=3"
        QueryString(query)


    def test_get_string(self):
        query = "key1=value1&key2=한글값&key3=3"
        qs = QueryString(query)
        self.assertEqual(qs.get_param('key1'), 'value1')


    def test_get_hangul(self):
        query = "key1=value1&key2=한글값&key3=3"
        qs = QueryString(query)
        self.assertEqual(qs.get_param('key2'), '한글값')


    def test_get_int(self):
        query = "key1=value1&key2=한글값&key3=3"
        qs = QueryString(query)
        self.assertEqual(qs.get_int('key3'), 3)


    def test_get_array(self):
        query = "key1=a&key1=b"
        qs = QueryString(query)
        self.assertListEqual(qs.get_array_param('key1'), ['a', 'b'])


    def test_unset(self):
        query = 'key1=a'
        qs = QueryString(query)
        qs.unset('key1')
        self.assertEqual(qs.get_param('key1'), None)