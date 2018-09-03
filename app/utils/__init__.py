# -*- coding: utf-8 -*-

"""

Author: Y.Han Lee

"""


from __future__ import absolute_import
from .request_id import RequestID, current_request_id
from .filters import RequestIDLogFilter
from . import parser


__version__ = '0.9.3'


__all__ = [
    'RequestID',
    'current_request_id',
    'RequestIDLogFilter',
    'parser'
]


import flask
from app.utils.request import QueryString



def request_query():
    query_string = str(flask.request.query_string, encoding='utf-8')
    return QueryString(query_string)





