from app import db


class Dept(db.Model):
    """
    이 클래스는 부서정보를 저장하는 테이블에 대한 구조를 정의하는 클래스이다.

    Attributes:
        deptno  부서 번호
        dname   부서 이름
        loc     부서 위치
    """


    __tablename__ = 'dept'
    # __table_args__ = {"schema": "dev"}


    deptno = db.Column(db.Integer, primary_key=True)

    dname = db.Column(db.String(14))

    loc = db.Column(db.String(13))



    def to_json(self):
        """
        부서정보 데이터를 JSON(dict) 형식으로 변환 한다.

        :return: 부서정보 JSON
        """
        json = {
            'deptno': self.deptno,
            'dname': self.dname,
            'loc': self.loc,
        }
        return json


    def __init__(self, deptno=None, dname=None, loc=None):
        self.deptno = deptno
        self.dname = dname
        self.loc = loc

    def __repr__(self):
        return '{}=[{}, {}]'.format(self.dname, self.deptno, self.loc)