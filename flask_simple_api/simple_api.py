import functools
import gzip
import inspect
import json

from io import TextIOWrapper, BytesIO

import logbook

from flask import jsonify, request
from flask.ext.restful import reqparse
from sentinels import NOTHING
from werkzeug.exceptions import HTTPException

_logger = logbook.Logger(__name__)


def error_abort(message, code=400):
    _logger.error('Error {code} when processing response {r.method} {r.path}: {message}',
        r=request, message=message, code=code)
    response = jsonify({'message': message})
    response.status_code = code
    raise HTTPException(response=response)


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

        defaults = dict(zip(reversed(argspec.args),
                            reversed(argspec.defaults or ())))

        for (arg_name, expected_type) in argspec.annotations.items():
            self.types[arg_name] = expected_type
            default = defaults.get(arg_name, NOTHING)
            if default is not NOTHING:
                self.defaults[arg_name] = default

    def parse_kwargs(self):
        json = self._get_json()
        if json is None:
            error_abort('Request body does not contain a JSON document')
        returned = {}

        for arg_name, expected_type in self.types.items():
            value = json.get(arg_name, NOTHING)
            if value is NOTHING:
                value = self.defaults.get(arg_name, NOTHING)
            elif not isinstance(value, expected_type):
                error_abort(
                    'Value for parameter {!r} is of unexpected type (got {!r}, expected {!r})'.format(arg_name, value, expected_type))

            if value is NOTHING:
                error_abort('Parameter is missing: {!r}'.format(arg_name))
            returned[arg_name] = value
        return returned

    def _get_json(self):
        if not self._is_json_request():
            return None

        if request.headers.get('content-encoding') != 'gzip':
            return request.get_json(silent=True)

        s = BytesIO(request.data)

        with gzip.GzipFile(fileobj=s, mode='r') as f, TextIOWrapper(f) as w:
            try:
                return json.load(w)
            except (ValueError,):
                error_abort('Invalid JSON content')

    def _is_json_request(self):
        mt = request.mimetype
        return mt == 'application/json' or (mt.startswith('application/') and mt.endswith('+json'))
