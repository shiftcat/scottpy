"""
{
    "deptno": 10,
    "dname": "ACCOUNTING",
    "loc": "NEW YORK"
}
"""

DEPT_SCHEMA = \
    {
        "definitions": {},
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "http://example.com/root.json",
        "type": "object",
        "title": "The Dept Schema",
        "required": [
            "deptno",
            "dname",
            "loc"
        ],
        "properties": {
            "deptno": {
                "$id": "#/properties/deptno",
                "type": "integer",
                "minimum": 0,
                "maximum": 1000,
                "title": "The Deptno Schema",
                "examples": [
                    10
                ]
            },
            "dname": {
                "$id": "#/properties/dname",
                "type": "string",
                "minLength": 2,
                "maxLength": 14,
                "title": "The Dname Schema",
                "examples": [
                    "ACCOUNTING"
                ]
            },
            "loc": {
                "$id": "#/properties/loc",
                "type": "string",
                "minLength": 2,
                "maxLength": 13,
                "title": "The Loc Schema",
                "examples": [
                    "NEW YORK"
                ]
            }
        }
    }
