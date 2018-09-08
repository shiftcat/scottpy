
from sqlalchemy import ForeignKey
from app import db

from app.models.dept_model import Dept


class Emp(db.Model):
    """
    이 클래스는 사원정보를 저장하는 테이블의 구조의 정의하는 클래스이다.


    Attributes:
        empno   사원 번호
        ename   사원 이름
        job     업무
        mgr     관리자 사번
        hiredate    입사일자
        sal     급여
        comm    커미션
        deptno  소속 부서 번호
        dept    소숙 부서 정보

    """

    __tablename__ = 'emp'
    # __table_args__ = {"schema": "dev"}


    empno = db.Column(db.Integer, primary_key=True)

    ename = db.Column(db.String(10))

    job = db.Column(db.String(9))

    mgr = db.Column(db.Integer)

    hiredate = db.Column(db.Date)

    sal = db.Column(db.Float(7, 2))

    comm = db.Column(db.Float(7, 2))

    deptno = db.Column(db.Integer, ForeignKey(Dept.deptno))

    dept = db.relationship(Dept, foreign_keys=deptno)



    def to_json(self, dept: Dept=None) -> dict:
        """
        사원 정보를 JSON(dict) 형태로 변환 한다.

        :param dept: 사원의 소속 부서 정보
        :return: 사원 정보 JSON(dict)
        """

        json = {
            'empno': self.empno,
            'ename': self.ename,
            'job': self.job,
            'mgr': self.mgr,
            # 'hiredate': self.hiredate.strftime('%Y-%m-%d %H:%M:%S'),
            'hiredate': self.hiredate.strftime('%Y-%m-%d'),
            'sal': self.sal,
            'comm': self.comm
        }

        if dept:
            json['dept'] = dept.to_json()
        else:
            json['deptno'] = self.deptno
        return json


    # def __init__(self, empno, ename, job, mgr, hiredate, sal, comm, deptno, dept):
    #     self.empno = empno
    #     self.ename = ename
    #     self.job = job
    #     self.mgr = mgr
    #     self.hiredate = hiredate
    #     self.sal = sal
    #     self.comm = comm
    #     self.deptno = deptno
    #     self.dept = dept


    def __repr__(self):
        return '{}=[{}, {}]'.format(self.ename, self.empno, self.deptno)
