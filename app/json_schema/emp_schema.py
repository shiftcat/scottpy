"""
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

"""

EMP_SCHEMA = \
    {
        "definitions": {},
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "http://example.com/root.json",
        "type": "object",
        "title": "The Emp Schema",
        "minProperties": 0,
        "required": [
            "empno",
            "ename",
            "job",
            "mgr",
            "hiredate"
        ],
        "properties": {
            "empno": {
                "$id": "#/properties/empno",
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000,
                "title": "The Empno Schema",
                "examples": [
                    8900
                ]
            },
            "ename": {
                "$id": "#/properties/ename",
                "type": "string",
                "minLength": 2,
                "maxLength": 10,
                "title": "The Ename Schema",
                "examples": [
                    "NEWWMP"
                ]
            },
            "job": {
                "$id": "#/properties/job",
                "type": "string",
                "minLength": 2,
                "maxLength": 9,
                "title": "The Job Schema",
                "examples": [
                    "ANALYST"
                ]
            },
            "mgr": {
                "$id": "#/properties/mgr",
                "type": [
                    "integer",
                    "null"
                ],
                "title": "The Mgr Schema",
                "examples": [
                    7782
                ]
            },
            "hiredate": {
                "$id": "#/properties/hiredate",
                "type": "string",
                "title": "The Hiredate Schema",
                "examples": [
                    "1982-11-09"
                ],
                "format": "date"
            },
            "sal": {
                "$id": "#/properties/sal",
                "type": "number",
                "minimum": 0,
                "maximum": 99999,
                "title": "The Sal Schema",
                "default": 0,
                "examples": [
                    5000
                ]
            },
            "comm": {
                "$id": "#/properties/comm",
                "type": [
                    "number",
                    "null"
                ],
                "minimum": 0,
                "maximum": 99999,
                "title": "The Comm Schema",
                "examples": [
                    900
                ]
            },
            "deptno": {
                "$id": "#/properties/deptno",
                "type": "integer",
                "title": "The Deptno Schema",
                "examples": [
                    20
                ]
            }
        }
    }
