
import json
from flask import Response
from .request_id import flask_ctx_get_request_id

def json_template(result:dict, count:int=0, status:int=200) -> dict:
    json_data = {}
    json_data['status'] = status
    if count:
        json_data['count'] = count
    else:
        json_data['count'] = len(result)
    json_data['result'] = result
    json_data['request_id'] = flask_ctx_get_request_id()
    return json_data


def json_render(data:dict) -> Response:
    status = data['status']
    json_data = json.dumps(data, ensure_ascii=False)
    return Response(json_data, status=status, mimetype='application/json')