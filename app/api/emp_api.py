# -*- coding: utf-8 -*-

"""
 이 모듈은 사원 관리 API를 제공하기 위한 모듈이다.

"""

from flask import request
from flask_restplus import Resource, Namespace, fields, reqparse
import validictory


from app.json_schema.emp_schema import EMP_SCHEMA

from app.utils.response import json_template
from app.utils import request_query

from app.biz.emp import EmployeeBiz
from app.api import ResponseSchem, ResponseModel
from app.api.dept_api import dept_model


ns_emp = Namespace("emp", description="사원 관리 API")

biz = EmployeeBiz()


# 사원 조회 API에서 사용될 파라미터
emp_search_args = reqparse.RequestParser()
emp_search_args.add_argument('ename', type=str, required=False, help='사원명')
emp_search_args.add_argument('deptno', type=int, required=False, choices=[10, 20, 30, 40, 50], default=10, help='부서번호')
emp_search_args.add_argument('size', type=int, required=False, help='조회결과 개수')
emp_search_args.add_argument('offset', type=int, required=False, help='조회시작 위치')

# 부서 정보가 포함되지 않은 사원정보 구조
emp_base_schem = {
    'empno': fields.Integer(required=True, description='사원 번호', example=8900),
    'ename': fields.String(required=True, description='사원의 이름', min_length=2, max_length=10, example='홍길동'),
    'job': fields.String(required=True, description='사원의 역할', min_length=2, max_length=9, example='개발자'),
    'mgr': fields.Integer(required=False, description='관리자 사원 번호', example=7782),
    'hiredate': fields.Date(required=True, description='YYYY-MM-DD 형식의 사원 생일', example='2018-01-01'),
    'sal': fields.Float(required=True, description='사원 급여', min=0, max=99999, example=9000),
    'comm': fields.Float(required=False, description='사원 보너스', min=0, max=99999, example=9000),
}

# 위 사원정보에 부서번호를 포함한 모델.
emp_schem = emp_base_schem.copy()
emp_schem['deptno'] = fields.Integer(required=False, description='사원의 소속 부서', example=10)
emp_model = ns_emp.model('Emp', emp_schem)

# 위 사원정보에 부서 정보를 포함한 모델.
emp_with_dept_schem = emp_base_schem.copy()
emp_with_dept_schem['dept'] = fields.Nested(dept_model)
emp_whith_dept_model = ns_emp.model('EmpWithDept', emp_with_dept_schem)

# 사원정보 조회시 결과 모델
search_schem = ResponseSchem.success.copy()
search_schem['result'] = fields.List(fields.Nested(emp_whith_dept_model))
search_result_model = ns_emp.model('EmpSearch', search_schem)

# 하나의 사원 정보 모델.
emp_result_schem = ResponseSchem.success.copy()
emp_result_schem['result'] = fields.Nested(emp_whith_dept_model)
emp_result_model = ns_emp.model('EmpResult', emp_result_schem)


@ns_emp.route('/search')
class EmpSearch(Resource):

    @ns_emp.expect(emp_search_args, validate=True)
    @ns_emp.response(200, '요청한 처리를 성공으로 완료 함.', model=search_result_model)
    @ns_emp.response(404, '조회결과가 존재하지 않음.', model=ResponseModel.not_found)
    @ns_emp.marshal_with(search_result_model)
    def get(self):
        """
        이 API는 사원정보를 조회하는 API이다.

        # Query string parameters
        * ename: like 조건에 사용 될 사원의 이름
        * deptno: 부서 번호
        * size: 조회결과의 사원정보 갯수. 기본값은 10이며 최대 1000개로 제한 한다.
        * offset: 조회 시작 위치. 기본값은 0이다.

        # Example
        ```
        /search?ename=MI&deptno=10size=30&offset=0
        ```

        """
        qs = request_query()
        ename = qs.get_param('ename', '')
        deptno = qs.get_int('deptno', 0)
        size = qs.get_int('size', 10)
        offset = qs.get_int('offset', 0)
        if size > 1000:
            size = 1000

        emp_list = biz.get_emp_list(ename, deptno, size, offset)
        json = json_template(emp_list)
        return json


@ns_emp.param('empno', '사원번호')
@ns_emp.route('/<int:empno>')
class EmpApi(Resource):

    @ns_emp.response(200, '요청한 처리를 성공으로 완료 함.', model=emp_result_model)
    @ns_emp.response(404, '사번에 대한 사원정보가 존재하지 않음.', model=ResponseModel.not_found)
    @ns_emp.marshal_with(emp_result_model)
    def get(self, empno):
        """
        이 API는 사원번호(empno)에 해당 하는 사원정보를 조회 한다.

        """
        emp = biz.get_emp(empno)
        json = json_template(emp, 1)
        return json


    @ns_emp.response(200, '요청한 처리를 성공으로 완료 함.', model=ResponseModel.success)
    @ns_emp.response(404, '사번에 대한 사원정보가 존재하지 않음.', model=ResponseModel.not_found)
    @ns_emp.marshal_with(ResponseModel.success)
    def delete(self, empno):
        """
        이 API는 사원번호(empno)에 해당 하는 사원정보를 삭제 한다.

        """
        biz.del_emp(empno)
        json = json_template("OK", 1)
        return json


# json_parser = ns_emp.parser()
# json_parser.add_argument('json', type=str, required=True, location='json',
#                          help='JSON BODY argument')
# arg_parser = ns_emp.parser()
# arg_parser.add_argument('json', type=str, required=True,
#                         help='URL JSON argument')

@ns_emp.route('')
class EmpSave(Resource):

    @ns_emp.expect(emp_model)
    @ns_emp.response(200, '요청한 처리를 성공으로 완료 함.', model=search_result_model)
    @ns_emp.response(400, '입력한 JSON 문서내 필수 항목이 누락 되었거나 유효하지 않은 값이 존재 함.', model=ResponseModel.bad_request)
    @ns_emp.response(404, '부서번호 또는 관리자 사번이 존재하지 않음.', model=ResponseModel.not_found)
    @ns_emp.marshal_with(search_result_model)
    def post(self):
        """
        이 API는 사원 정보를 등록하는 API이다.

        사원번호(empno) 해당하는 사원정보가 존재하지 않으면 신규로 사원을 등록하고 존재하면 그 사원의 정보를 변경한다.
        * mgr 항목은 관리자 사번으로 그 사번에 해당하는 사원정보가 존재햐야 한다.
        * deptno 항목은 부서번호로 반드시 존재하는 부서번호 이어야 한다.

        # Example
        ```json
        {
            "empno": 8900,
            "ename": "NEWWMP",
            "job": "ANALYST",
            "mgr": 7782,
            "hiredate": "1982-11-09",
            "sal": 5000,
            "comm": null,
            "deptno": 20
        }
        ```

        """
        input_json = request.json
        validictory.validate(input_json, EMP_SCHEMA, fail_fast=False)

        emp = biz.add_emp(input_json)

        json = json_template(emp, 1)
        return json