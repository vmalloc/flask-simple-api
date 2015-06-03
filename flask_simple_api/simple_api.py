import functools
import inspect

from flask import abort, jsonify, request
from flask.ext.restful import reqparse
from sentinels import NOTHING


def api(app_or_blueprint, name=None):

    def decorator(func):

        nonlocal name

        if name is None:
            name = func.__name__

        parser = Parser(func)

        @app_or_blueprint.route('/{}'.format(name), methods=['POST'], endpoint=name)
        @functools.wraps(func)
        def new_func():
            kwargs = parser.parse_kwargs()
            returned = func(**kwargs)
            return jsonify({'result': returned})
        return new_func
    return decorator

class Parser(object):

    def __init__(self, func):
        super(Parser, self).__init__()
        self.types = {}
        self.defaults = {}

        while True:
            wrapped = getattr(func, '__wrapped__', None)
            if not wrapped:
                break
            func = wrapped

        argspec = inspect.getfullargspec(func)

        defaults = dict(zip(reversed(argspec.args), reversed(argspec.defaults or ())))

        for (arg_name, expected_type) in argspec.annotations.items():
            self.types[arg_name] = expected_type
            default = defaults.get(arg_name, NOTHING)
            if default is not NOTHING:
                self.defaults[arg_name] = default

    def parse_kwargs(self):
        json = request.json
        returned = {}

        for arg_name, expected_type in self.types.items():
            value = json.get(arg_name, NOTHING)
            if value is NOTHING:
                value = self.defaults.get(arg_name, NOTHING)
            elif not isinstance(value, expected_type):
                abort(400)

            if value is NOTHING:
                abort(400)
            returned[arg_name] = value
        return returned
