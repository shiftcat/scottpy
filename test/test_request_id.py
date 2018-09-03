
from app.utils import RequestID
from app.utils import current_request_id

from flask import Flask


flask_app = Flask(__name__)

RequestID(flask_app)


@flask_app.route('/hello')
def hello():
    print('Current request id: {}'.format(current_request_id()))
    return "Hello"



flask_app.test_client().get('/hello')