# -*- coding: utf-8 -*-

"""
 이 모듈은 부서 관리 API를 제공하기 위한 모듈이다.

"""

from flask import request
from flask_restplus import Resource, Namespace, fields
import validictory

from app.utils.response import json_template
from app.biz.dept import DepartmentBiz
from app.json_schema.dept_schema import DEPT_SCHEMA
from app.api import ResponseSchem, ResponseModel



ns_dept = Namespace("dept", description="부서 관리 API")

biz = DepartmentBiz()


dept_schem = {
    'deptno': fields.Integer(required=True, description='부서 번호', example=50),
    'dname': fields.String(required=True, description='부서명', min_length=2, max_length=14, example='연구소'),
    'loc': fields.String(required=True, description='부서 위치', min_length=2, max_length=13, example='서울 중구'),
}

dept_model = ns_dept.model('Dept', dept_schem)

search_schem = ResponseSchem.success.copy()
search_schem['result'] = fields.List(fields.Nested(dept_model))
search_result_model = ns_dept.model('DeptSearch', search_schem)


dept_result_schem = ResponseSchem.success.copy()
dept_result_schem['result'] = fields.Nested(dept_model)
dept_result_model = ns_dept.model('DeptResult', dept_result_schem)


@ns_dept.route('/search')
class DeptSearch(Resource):

    @ns_dept.response(200, '요청한 처리를 성공으로 완료 함.', model=search_result_model)
    @ns_dept.marshal_with(search_result_model)
    def get(self):
        """
        이 API는 부서정보를 조회하는 API이다.

        """
        dept_list = biz.get_dept_list()
        json = json_template(dept_list)
        return json


@ns_dept.param('deptno', '부서번호')
@ns_dept.route("/<int:deptno>")
class DeptApi(Resource):

    @ns_dept.response(200, '요청한 처리를 성공으로 완료 함.', model=dept_result_model)
    @ns_dept.response(404, '부서번호에 대한 부서정보가 존재하지 않음.', model=ResponseModel.not_found)
    @ns_dept.marshal_with(dept_result_model)
    def get(self, deptno):
        """
        이 API는 부서번호(deptno)에 해당하는 부서정보를 조회 한다.

        """
        dept = biz.get_dept(deptno)
        json = json_template(dept, 1)
        return json

    @ns_dept.response(200, '요청한 처리를 성공으로 완료 함.', model=ResponseModel.success)
    @ns_dept.response(404, '부서번호에 대한 부서정보가 존재하지 않음.', model=ResponseModel.not_found)
    @ns_dept.marshal_with(ResponseModel.success)
    def delete(self, deptno):
        """
        이 API는 부서번호(deptno)에 해당하는 부서정보를 삭제 한다.

        """
        biz.del_dpet(deptno)
        json = json_template("OK", 1)
        return json



@ns_dept.route("")
class DeptSave(Resource):

    @ns_dept.expect(dept_model)
    @ns_dept.response(200, '요청한 처리를 성공으로 완료 함.', model=dept_result_model)
    @ns_dept.response(400, '입력한 JSON 문서내 필수 항목이 누락 되었거나 유효하지 않은 값이 존재 함.', model=ResponseModel.bad_request)
    @ns_dept.marshal_with(dept_result_model)
    def post(self):
        """
        이 API는 부서 정보를 등록하는 API이다.

        부서번호(deptno) 해당하는 부서정보가 존재하지 않으면 신규로 등록하고 존재하면 그 부서의 정보를 변경한다.

        # Example
        ```json
        {
            "deptno": 50,
            "dname": "연구소",
            "loc": "서울 중구"
        }
        ```

        """
        input_json = request.json
        validictory.validate(input_json, DEPT_SCHEMA, fail_fast=False)
        dept = biz.add_dept(input_json)
        json = json_template(dept, 1)
        return json


