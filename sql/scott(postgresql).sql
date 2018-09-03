
/*
postgres 관리자 계정으로
scott 관리자, 개발자 계정 및 테이블스페이스(scott_sapce), 데이터베이스(scott_db) 생성

scott_admin: 테이블 생성 변경 등의 관리자 계정
scott_dev: 데이터의 조회, 수정, 삭제 등의 개발자 계정

*/

-- 개발디비 관리자 계정 생성(테이블 생성 변경 등의 작업 관리용 계정)
CREATE USER scott_admin PASSWORD 'tmzktrhksflwk';

-- 개발자 계정 생성(데이터의 조회, 수정, 삭제 등의 작업용 계정)
CREATE USER scott_dev password 'tmzktroqkfwk';
ALTER USER scott_dev SET search_path='dev';


-- 테이블스페이스 생성 및 데이터베이스 생성
CREATE TABLESPACE scott_sapce OWNER scott_admin
  LOCATION 'tablespace directory path';

CREATE DATABASE scott_db
    WITH OWNER = scott_admin
         ENCODING = 'UTF8'
         TABLESPACE = 'scott_sapce';


-- postgres 계정으로 접속 후 public schema 삭제 (반드시 해야하는 작업은 아니다.)
DROP SCHEMA public;

 -- scott_admin 계정으로 scott_db 접속 후 schema 생성
CREATE SCHEMA dev;

-- 개발자계정에 생성된 스키마 사용권한 부여
GRANT USAGE ON SCHEMA dev TO scott_dev;



/*
dev 관리자 계정(scott_admin) 계정으로 로그인 후 테이블 생성 작업 실행
*/
DROP TABLE dev.EMP;
DROP TABLE dev.DEPT;
DROP TABLE dev.BONUS;
DROP TABLE dev.SALGRADE;
DROP TABLE dev.DUMMY;

CREATE TABLE dev.DEPT (
        DEPTNO integer NOT NULL,
        DNAME varchar(14) NOT NULL,
        LOC varchar(13) NOT NULL
);

ALTER TABLE dev.dept
  ADD CONSTRAINT dept_pk PRIMARY KEY(deptno);

INSERT INTO dev.DEPT VALUES (10, 'ACCOUNTING', 'NEW YORK');
INSERT INTO dev.DEPT VALUES (20, 'RESEARCH',   'DALLAS');
INSERT INTO dev.DEPT VALUES (30, 'SALES',      'CHICAGO');
INSERT INTO dev.DEPT VALUES (40, 'OPERATIONS', 'BOSTON');

SELECT * FROM dev.DEPT;


CREATE TABLE dev.EMP (
        EMPNO integer NOT NULL,
        ENAME varchar(10) NOT NULL,
        JOB varchar(9) NOT NULL,
        MGR integer,
        HIREDATE date NOT NULL,
        SAL numeric(7, 2) NOT NULL,
        COMM numeric(7, 2),
        DEPTNO integer
);

ALTER TABLE dev.emp
	ADD CONSTRAINT emp_pk PRIMARY KEY(empno);

ALTER TABLE dev.emp
  ADD CONSTRAINT deptno_fk FOREIGN KEY (deptno) REFERENCES dev.dept (deptno);


INSERT INTO dev.EMP VALUES(7369,'SMITH','CLERK',7902,to_date('17-12-1980','dd-mm-yyyy'),800,NULL,20);
INSERT INTO dev.EMP VALUES(7499,'ALLEN','SALESMAN',7698,to_date('20-2-1981','dd-mm-yyyy'),1600,300,30);
INSERT INTO dev.EMP VALUES(7521,'WARD','SALESMAN',7698,to_date('22-2-1981','dd-mm-yyyy'),1250,500,30);
INSERT INTO dev.EMP VALUES(7566,'JONES','MANAGER',7839,to_date('2-4-1981','dd-mm-yyyy'),2975,NULL,20);
INSERT INTO dev.EMP VALUES(7654,'MARTIN','SALESMAN',7698,to_date('28-9-1981','dd-mm-yyyy'),1250,1400,30);
INSERT INTO dev.EMP VALUES(7698,'BLAKE','MANAGER',7839,to_date('1-5-1981','dd-mm-yyyy'),2850,NULL,30);
INSERT INTO dev.EMP VALUES(7782,'CLARK','MANAGER',7839,to_date('9-6-1981','dd-mm-yyyy'),2450,NULL,10);
INSERT INTO dev.EMP VALUES(7788,'SCOTT','ANALYST', 7566, to_date('13-7-1987', 'dd-mm-yyyy'), 3000,NULL,20);
INSERT INTO dev.EMP VALUES(7839,'KING','PRESIDENT',NULL,to_date('17-11-1981','dd-mm-yyyy'),5000,NULL,10);
INSERT INTO dev.EMP VALUES(7844,'TURNER','SALESMAN',7698,to_date('8-9-1981','dd-mm-yyyy'),1500,0,30);
INSERT INTO dev.EMP VALUES(7876,'ADAMS','CLERK',7788,to_date('13-7-1987', 'dd-mm-yyyy'), 1100,NULL,20);
INSERT INTO dev.EMP VALUES(7900,'JAMES','CLERK',7698,to_date('3-12-1981','dd-mm-yyyy'),950,NULL,30);
INSERT INTO dev.EMP VALUES(7902,'FORD','ANALYST',7566,to_date('3-12-1981','dd-mm-yyyy'),3000,NULL,20);
INSERT INTO dev.EMP VALUES(7934,'MILLER','CLERK',7782,to_date('23-1-1982','dd-mm-yyyy'),1300,NULL,10);


SELECT * FROM dev.EMP;



CREATE TABLE dev.BONUS (
        ENAME varchar(10) NOT NULL,
        JOB   varchar(9) NOT NULL,
        SAL   numeric(7, 2) NOT NULL,
        COMM  numeric(7, 2)
);

CREATE TABLE dev.SALGRADE (
        GRADE integer NOT NULL,
        LOSAL integer NOT NULL,
        HISAL integer NOT NULL
);

INSERT INTO dev.SALGRADE VALUES (1,  700, 1200);
INSERT INTO dev.SALGRADE VALUES (2, 1201, 1400);
INSERT INTO dev.SALGRADE VALUES (3, 1401, 2000);
INSERT INTO dev.SALGRADE VALUES (4, 2001, 3000);
INSERT INTO dev.SALGRADE VALUES (5, 3001, 9999);


-- 개발자 계정에 각 테이블에 권한 부여
GRANT select, insert, update, delete ON TABLE dev.dept TO scott_dev;
GRANT select, insert, update, delete ON TABLE dev.emp TO scott_dev;
GRANT select, insert, update, delete ON TABLE dev.bonus TO scott_dev;
GRANT select, insert, update, delete ON TABLE dev.salgrade TO scott_dev;
