

import logging
from app.utils import RequestIDLogFilter, RequestID
from flask import Flask


class AppLogging():

    def __init__(self):
        self.logger = logging.getLogger('scott.api')


    def __call__(self, *args, **kwargs):
        return self.logger


    def __get_stream_handler(self, formatter):
        stream_hander = logging.StreamHandler()
        stream_hander.setLevel(logging.DEBUG)
        stream_hander.setFormatter(formatter)
        stream_hander.addFilter(RequestIDLogFilter())
        return stream_hander


    def __init_logger(self, level):
        if len(self.logger.handlers) > 0:
            return
        self.logger.setLevel(level)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(request_id)s] [%(filename)s:%(lineno)s] > %(message)s')
        stream_hander = self.__get_stream_handler(formatter)
        self.logger.addHandler(stream_hander)


    LOG_LEVEL = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'error': logging.ERROR,
        'warn': logging.WARNING
    }


    def init_logging(self, flask: Flask):
        RequestID(flask)
        level_val = flask.config.get('LOG_LEVEL')
        log_level = AppLogging.LOG_LEVEL.get(level_val)
        self.__init_logger(log_level)


applogging = AppLogging()
logger = applogging()

