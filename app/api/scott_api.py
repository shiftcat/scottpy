# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restplus import Api, fields, Model

from validictory.validator import MultipleValidationError
from app.errors import ContentsNotFoundException
from app.utils.request_id import flask_ctx_get_request_id


class ResponseSchem():
    """
    응답시 사용될 메시지의 구조 정의
    """
    success = {
        'status': fields.Integer(required=True, description='응답코드', example=200),
        'count': fields.Integer(required=True, description='적용건수', example=1),
        'result': fields.String(required=True, description='메시지', example='OK'),
        'request_id': fields.String(required=True, description='Request ID', example='babb09e8-2423-4a70-8920-ba4e84aa13e9'),
    }
    not_found = {
        'status': fields.Integer(required=True, description='응답코드', example=404),
        'message': fields.String(required=True, description='메시지', example='Not found resource'),
        'request_id': fields.String(required=True, description='Request ID',
                                    example='babb09e8-2423-4a70-8920-ba4e84aa13e9'),
    }
    bad_request = {
        'status': fields.Integer(required=True, description='응답코드', example=400),
        'messages': fields.List(fields.String),
        'request_id': fields.String(required=True, description='Request ID',
                                    example='babb09e8-2423-4a70-8920-ba4e84aa13e9'),
    }


class ResponseModel():
    """
    응답시 사용될 메시지의 구조에 대한 모델 정의
    """
    success = Model('Success', ResponseSchem.success)
    not_found = Model('NotFound', ResponseSchem.not_found)
    bad_request = Model('BadRequest', ResponseSchem.bad_request)


def __add_models(api:Api):
    api.models[ResponseModel.success.name] = ResponseModel.success
    api.models[ResponseModel.not_found.name] = ResponseModel.not_found
    api.models[ResponseModel.bad_request.name] = ResponseModel.bad_request


def init_api():
    """
    API모듈을 초기화 하여 그 인스턴스를 리턴한다.

    :return: api instance
    """
    api = Api(version='1.0', title='Scott API', description='Scott API')
    __add_models(api)

    @api.errorhandler(MultipleValidationError)
    def validation_error(e):
        """
        입력한 JSON의 형식이 올바르지 않을 경우 발생한 에러를 처리하기 위한 함수이다.
        :param e: 에러객체
        :return: 에러메시지
        """
        json = {
            'status': 400,
            'messages': [str(el) for el in e.errors],
            'request_id': flask_ctx_get_request_id()
        }
        return json, 400


    @api.errorhandler(ContentsNotFoundException)
    def content_not_found_error(e):
        """
        조회결과가 존재하지 않을 경우 발생한 에러를 처리하기 위한 함수이다.
        :param e: 에러객체
        :return: 에러메시지
        """
        json = {
            'status': e.get_status(),
            'message': e.get_message(),
            'request_id': flask_ctx_get_request_id()
        }
        return json, e.get_status()


    @api.errorhandler
    def default_error_handler(e):
        """
        기본 에러 핸들러 함수
        :param e: 에러객체
        :return: 에러메시지
        """
        json = {
            'status': 500,
            'message': "Internal server error.",
            'request_id': flask_ctx_get_request_id()
        }
        return json, 500


    from . import dept_api, emp_api

    api.add_namespace(dept_api.ns_dept, path="/dept")
    api.add_namespace(emp_api.ns_emp, path="/emp")

    blueprint = Blueprint('api', __name__)
    api.init_app(blueprint)

    return blueprint






