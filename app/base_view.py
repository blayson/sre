from flask import jsonify
from flask.views import MethodView
from . import LOGGER


class BaseView(MethodView):
    _endpoint_name: str
    _name: str

    @classmethod
    def register(cls, blueprint):
        method_view = cls.as_view(cls._name)
        blueprint.add_url_rule(cls._endpoint_name, view_func=method_view)
        blueprint.register_error_handler(422, cls.handle_error)

    @staticmethod
    def handle_error(err):
        headers = err.data.get('headers', None)
        messages = err.data.get('messages', ['Invalid Request.'])
        LOGGER.warning(f'Invalid input params: {messages}')
        if headers:
            return jsonify({'msg': messages}), 400, headers
        else:
            return jsonify({'msg': messages}), 400
