import functools
import json
import uuid

import logbook
import requests

import pytest
from flask import Flask
from flask.ext.loopback import FlaskLoopback
from flask.ext.simple_api import SimpleAPI


@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    logbook.StderrHandler(level=logbook.DEBUG).push_application()


@pytest.fixture
def call_api(webapp):
    def callable(_name, **kwargs):
        resp = webapp.post(
            '/{}'.format(_name), data=json.dumps(kwargs), headers={'Content-type': 'application/json'})
        return resp['result']
    return callable

def _decorator(func):

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        return func(*args, **kwargs)
    return new_func

@pytest.fixture
def webapp(request):
    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['DEBUG'] = True

    api = SimpleAPI(app)

    @api.include
    def api_no_args():
        return 'ok no args'

    @api.include
    def sum(a: int, b: int, c: int=3):
        return a + b + c

    @api.include
    def mul(a: int, b: int): # use direct types
        return a * b

    @api.include
    @_decorator
    def div(a: int, b: int): # use decorator
        return a / b

    @api.include
    def echo(list_value: list, dict_value: dict):
        return [list_value, dict_value]

    @api.include
    def default_to_none(str_value: str=None):
        return 'Got {!r}'.format(str_value)


    returned = Webapp(app)
    returned.activate()
    request.addfinalizer(returned.deactivate)
    return returned


class Webapp(object):

    def __init__(self, app):
        super(Webapp, self).__init__()
        self.app = app
        self.loopback = FlaskLoopback(self.app)
        self.hostname = str(uuid.uuid1())

    def activate(self):
        self.loopback.activate_address((self.hostname, 80))

    def deactivate(self):
        self.loopback.deactivate_address((self.hostname, 80))

    def _request(self, method, path, *args, **kwargs):
        raw_response = kwargs.pop("raw_response", False)
        if path.startswith("/"):
            path = path[1:]
            assert not path.startswith("/")
        returned = requests.request(
            method, "http://{0}/{1}".format(self.hostname, path), *args, **kwargs)
        if raw_response:
            return returned

        returned.raise_for_status()
        return returned.json()


def _make_request_shortcut(method_name):
    def json_method(self, *args, **kwargs):
        return self._request(method_name, *args, **kwargs)

    json_method.__name__ = method_name
    setattr(Webapp, method_name, json_method)

    def raw_method(self, *args, **kwargs):
        return self._request(method_name, raw_response=True, *args, **kwargs)

    raw_method.__name__ = "{0}_raw".format(method_name)
    setattr(Webapp, raw_method.__name__, raw_method)

for _method in ("get", "put", "post", "delete"):
    _make_request_shortcut(_method)
