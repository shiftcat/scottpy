# -*- coding: utf-8 -*-

from datetime import datetime

from app import db, transactional, logger

from app.errors import ContentsNotFoundException

from app.models.emp_model import Emp
from app.models.dept_model import Dept

from app.biz.dept import DepartmentBiz


dept_biz = DepartmentBiz()


class EmployeeBiz():
    """
    이 클래스는 사원정보를 관리하기 위한 클래스 이다.
    """


    def __init__(self):
        pass


    def get_emp_list(self, ename:str=None, deptno:int=0, size=10, offset=0):
        """
        사원 정보를 조회하여 목록을 리턴한다.
        :param ename: 사원명
        :param deptno: 부서번호
        :param size: 조회 크기
        :param offset: 조회 시작 위치
        :return: 사원 목록
        """
        logger.debug("get_emp_list begin")
        sql = db.session.query(Emp, Dept).join(Dept)
        if ename:
            sql = sql.filter(Emp.ename.like("%{}%".format(ename)))
        if deptno:
            sql = sql.filter(Dept.deptno == deptno)

        rows = sql.order_by(Emp.empno.asc()).limit(size).offset(offset)

        emp_list = []
        for row in rows:
            emp_list.append(row.Emp.to_json(row.Dept))

        if not emp_list:
            raise ContentsNotFoundException('Emp not found.')
        logger.debug("get_emp_list end")
        return emp_list


    def get_emp_object(self, empno:int) -> Emp:
        """
        empno에 해당하는 사원 정보를 조회하여 Emp 모델 객체를 리턴한다.
        :param empno:
        :return: 사원 모델 객체
        """
        return db.session.query(Emp).filter(Emp.empno == empno).first()


    def get_emp(self, empno:int) -> dict:
        """
        empno에 해당하는 사원정보를 조회하여 리턴한다.
        :param empno: 사번
        :return: 사원 정보
        """
        logger.debug("get_emp begin {}".format(empno))
        res = db.session.query(Emp, Dept).join(Dept).filter(Emp.empno == empno).first()
        if res is None:
            raise ContentsNotFoundException('Emp not found.')
        logger.debug("get_emp end")
        return res.Emp.to_json(res.Dept)


    def __set_emp_info(self, emp: Emp, json):
        emp.ename = json['ename']
        emp.deptno = json.get('deptno')
        emp.job = json['job']
        emp.hiredate = datetime.strptime(json['hiredate'], '%Y-%m-%d')
        emp.mgr = json.get('mgr')
        emp.comm = json.get('comm')
        emp.sal = json['sal']


    @transactional
    def add_emp(self, new_emp: dict) -> dict:
        """
        신규로 사원정보를 저장하거나 empno에 해당하는 사원 정보가 존재하면 그 사원정보를 변경한다.
        :param new_emp: 신규 또는 변경할 사원 정보
        :return: 저장된 사원 정보
        :raise ContentsNotFoundException: 부서번호 또는 관리자 사번이 존재하지 않을 경우 발생한다.
        """
        logger.debug("add_emp begin")
        dept = None
        if new_emp.get("deptno"):
            dept = dept_biz.get_dept_object(new_emp['deptno'])
            if dept is None:
                raise ContentsNotFoundException('Dept not found.')

        if new_emp.get("mgr"):
            mgr_emp = self.get_emp_object(new_emp['mgr'])
            if mgr_emp is None:
                raise ContentsNotFoundException('Manager not found.')

        emp = self.get_emp_object(new_emp['empno'])
        if emp is None:
            # insert
            emp = Emp()
            emp.empno = new_emp['empno']
            self.__set_emp_info(emp, new_emp)
            db.session.add(emp)
        else:
            # update
            self.__set_emp_info(emp, new_emp)
        logger.debug("add_emp end")
        return emp.to_json(dept)


    @transactional
    def del_emp(self, empno:int):
        """
        empno에 해당하는 사원정보를 삭제한다.

        :param empno: 사원번호
        """
        logger.debug("del_emp begin {}".format(empno))
        emp = self.get_emp_object(empno)
        if emp is None:
            raise ContentsNotFoundException('Emp not found.')
        logger.debug("del_emp end")
        db.session.delete(emp)