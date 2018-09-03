# Scott Flask RESTful Web service

이 프로젝트는 파이썬 플라스크를 이용하여 오라클 데이터베이스에서 scott 계정으로 제공되는 샘플 데이터를 RESTful API로 제공하는 샘플 프로젝트이다.


API의 한 호출당 고유 ID 부여 기능은 다음 모듈을 사용 하였다.

**https://github.com/Workable/flask-log-request-id**


### 프로젝트 환경
* Python 3.6
* SQLAlchemy 1.2.11
* validictory 1.1.2
* flask-restplus 0.11.0
* MySql 8.0 or SQLite


### 기능 및 특징
* 부서(DEPT), 사원(EMP) 관리 API 
* API 한 호출당 고유 ID 부여
* swagger를 이용하여 API문서 제공 - flask-restplus
* SQLAlchemy ORM Framework
* JSON schema validate - validictory


### docker run

```buildoutcfg
$ docker build -t scottpy:latest .

$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
scottpy             latest              c2da92094c3a        11 seconds ago      470MB

$ docker run -it --rm -p 5000:5000 --name scott.api scottpy:latest

$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS                    NAMES
ae876c8f7d64        scottpy:latest      "/bin/sh -c 'python3…"   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp   epic_goldstine

$ docker kill ae876c8f7d64
```

### Swagger API 문서
* API Document: http://localhost:5000/api/



