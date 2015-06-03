import json
import uuid

import requests
from flask import Flask
from flask.ext.loopback import FlaskLoopback
from flask.ext.simple_api import api, ARG

import pytest


@pytest.fixture
def call_api(webapp):
    def callable(_name, **kwargs):
        resp = webapp.post(
            '/{}'.format(_name), data=json.dumps(kwargs), headers={'Content-type': 'application/json'})
        return resp['result']
    return callable


@pytest.fixture
def webapp(request):
    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['DEBUG'] = True

    @api(app)
    def api_no_args():
        return 'ok no args'

    @api(app)
    def sum(a: ARG(type=int), b: ARG(type=int), c: ARG(type=int, default=3)):
        return a + b + c

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
