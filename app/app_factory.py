# -*- coding: utf-8 -*-




from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from app.utils.response import json_render
from app.api import init_api

from .applogging import logger, applogging


db = SQLAlchemy()


def __begin_tran():
    try:
        db.session.begin()
        return db.session
    except Exception as e:
        logger.warning(str(e))
        return db.session


def transactional(func):
    def wrapper(*args, **kwargs):
        tx = __begin_tran()
        try:
            res = func(*args, **kwargs)
            tx.commit()
            return res
        except Exception as e:
            tx.rollback()
            raise e
    return wrapper




def __init_config(flask_app, config):
    flask_app.config.from_object(config)
    applogging.init_logging(flask_app)
    db.init_app(flask_app)


def __init_request_log_handler(flask_app):

    @flask_app.before_request
    def before_request():
        logger.info("======= Request start =======")
        logger.info("remote ip: {}".format(getattr(request, 'remote_addr')))
        logger.info("Request URL: {}".format(getattr(request, 'url')))
        logger.info("Request data: {}".format(getattr(request, 'json')))
        logger.info("Request args: {}".format(getattr(request, 'args')))


    @flask_app.after_request
    def after_request(response):
        logger.info("====== after request ======")
        logger.info("Response Data {}".format(getattr(response, 'json')))
        # db.session.commit()
        return response


    # @flask_app.teardown_request
    # def teardown_request(exception):
    #     if exception:
    #         flask_app.logger.error("error => {}".format(str(exception)))
    #         db.session.rollback()
    #     else:
    #         flask_app.logger.debug("request complete!")
    #         db.session.commit()
    #     db.session.remove()



def __init_error_handler(flask_app):

    @flask_app.errorhandler(404)
    def error_handl_not_found(error):
        request_url = request.url
        json = {
            'status': 404,
            'message': 'request url \'{}\' not found.'.format(request_url)
        }
        return json_render(json)




def create_app(config:object):
    """
    Flask application를 초기화 하고 그 인스턴스를 리턴한다.
    :param config:
    :return: Flask application instance
    """
    logger.debug("=== Flask application start ===")
    flask_app = Flask(__name__)
    __init_config(flask_app, config)
    __init_request_log_handler(flask_app)
    __init_error_handler(flask_app)
    api = init_api()
    flask_app.register_blueprint(api, url_prefix='/api')

    return flask_app




if __name__ == "__main__":
    from .config import config
    flk_app = create_app(config['dev'])
    flk_app.run(port=5000)