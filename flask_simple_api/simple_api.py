import functools
import inspect

from flask import jsonify
from flask.ext.restful import reqparse


def api(app_or_blueprint, name=None):

    def decorator(func):

        nonlocal name

        if name is None:
            name = func.__name__

        parser, arg_names = _create_func_parser(func)

        @app_or_blueprint.route('/{}'.format(name), methods=['POST'], endpoint=name)
        @functools.wraps(func)
        def new_func():
            parsed_args = parser.parse_args()
            kwargs = {arg_name: getattr(parsed_args, arg_name) for arg_name in arg_names}
            returned = func(**kwargs)
            return jsonify({'result': returned})
        return new_func
    return decorator

class ARG(object):

    def __init__(self, **options):
        super(ARG, self).__init__()
        self.options = options
        if 'required' not in self.options:
            self.options['required'] = 'default' not in self.options


def _create_func_parser(func):
    returned = reqparse.RequestParser()
    arg_names = []
    for arg_name, annotation in inspect.getfullargspec(func).annotations.items():
        returned.add_argument(arg_name, **annotation.options)
        arg_names.append(arg_name)
    return returned, arg_names
