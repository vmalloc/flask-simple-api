import json

from flask import Flask

import pytest
from requests import HTTPError


def test_no_args(call_api):
    assert call_api('api_no_args') == 'ok no args'


def test_args(call_api):
    assert call_api('sum', a=1, b=2, c=5) == 8


def test_default_args(call_api):
    assert call_api('sum', a=1, b=2) == 6


def test_wrong_types(call_api):
    with pytest.raises(HTTPError) as caught:
        call_api('sum', a='b', b=2)
    assert caught.value.response.status_code == 400


def test_missing_args(call_api):
    with pytest.raises(HTTPError) as caught:
        call_api('sum', b=2)
    assert caught.value.response.status_code == 400


