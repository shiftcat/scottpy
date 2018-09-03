

from app import db, transactional

from app.errors import ContentsNotFoundException

from app.models.dept_model import Dept



class DepartmentBiz():
    """
    이 클래스는 부서관리를 위한 클래스이다.

    """

    def __init__(self):
        pass


    def get_dept_list(self) -> list:
        """
        부서 목록을 조회하여 리턴한다.
        :return: 부서목록
        """
        rows = db.session.query(Dept).all()
        dept_list = []
        for row in rows:
            dept_list.append(row.to_json())
        return dept_list


    def get_dept_object(self, deptno:int) -> Dept:
        """
        deptno에 해당하는 부서 정보를 조회하여 Dept 모델 객체를 리턴한다.
        :param deptno:
        :return: 부서정보 모델 객체
        """
        return db.session.query(Dept).filter(Dept.deptno == deptno).first()


    def get_dept(self, deptno) -> dict:
        """
        deptno 해당하는 부서정보를 조회하여 리턴한다.
        :param deptno: 부서번호
        :return: 부서정보
        """
        dept = self.get_dept_object(deptno)
        if dept is None:
            raise ContentsNotFoundException('Dept not found.')
        return dept.to_json()



    def __dept_info(self, dept:Dept, json):
        dept.deptno = json['deptno']
        dept.dname = json['dname']
        dept.loc = json['loc']


    @transactional
    def add_dept(self, new_dept:dict) -> dict:
        """
        신규로 부서정보를 저장하거나 deptno에 해당하는 부서정보 있다면  그 부서정보를 변경한다.
        :param new_dept: 신규 또는 변경 부서정보
        :return: 저장한 부서정보
        """
        dept = db.session.query(Dept).filter(Dept.deptno == new_dept['deptno']).first()
        if dept is None:
            # insert
            dept = Dept()
            self.__dept_info(dept, new_dept)
            db.session.add(dept)
        else:
            # Update
            self.__dept_info(dept, new_dept)

        return dept.to_json()


    @transactional
    def del_dpet(self, deptno:int):
        """
        deptno에 해당하는 부서정보를 삭제 한다.
        :param deptno: 부서번호
        """
        dept = db.session.query(Dept).filter(Dept.deptno == deptno).first()
        if dept is None:
            raise ContentsNotFoundException('Dept not found.')
        db.session.delete(dept)
