# -*- coding: utf-8 -*-

"""

Author: Y.Han Lee

"""

from urllib.parse import unquote
from urllib.parse import parse_qs
from urllib.parse import urlencode


class QueryString():
    """
    이 클래스는 URL에서 Query string을 위한 클래스 이다.

    """


    def __init__(self, query_string):
        """
        URL의 쿼리 스트링을 인자로 하는 생성자 함수이다.
        :param query_string:
        """
        self.query_string = query_string
        qs = unquote(self.query_string, encoding='utf-8')
        self.parsed_query = parse_qs(qs)


    def make_query(self):
        return urlencode(self.parsed_query, doseq=True)


    def get_param(self, key:str, default=None):
        if self.parsed_query.get(key):
            param = self.parsed_query.get(key)[0]
            if param:
                return param
            else:
                return default
        else:
            return default


    def get_int(self, key:str, default=0) -> int:
        if self.parsed_query.get(key):
            param = self.parsed_query.get(key)[0]
            if param:
                try:
                    intval = int(param)
                except:
                    intval = default
                return intval
            else:
                return default
        else:
            return default


    def get_array_param(self, key:str) -> list:
        if self.parsed_query.get(key):
            params = self.parsed_query.get(key)
            if params:
                return params
            else:
                return []
        else:
            return []


    def get_check_param(self, key:str, value, default=None) -> str:
        param = self.get_param(key, '')
        if param == value:
            return 'checked'
        elif value == default:
            return 'checked'


    def unset(self, key:str):
        if self.parsed_query.get(key):
            del self.parsed_query[key]



    def set_param(self, key:str, value):
        self.parsed_query[key] = value




if __name__ == '__main__':
    qs = QueryString('key1=1&key2=Hello+python&key3=%ED%8C%8C%EC%9D%B4%EC%8D%AC&arr1=1&arr1=2')
    print(qs.get_param('key1'))
    print(qs.get_param('param3', 'default_value'))
    print(qs.get_param('key3'))
    print(qs.get_array_param('arr1'))
    print(qs.make_string())
    qs.set_param('page', 1)
    print(qs.make_string())
    qs.unset('page')
    print(qs.make_string())