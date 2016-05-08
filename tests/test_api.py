import copy
import gzip
import json

from requests import HTTPError, codes

import pytest

from io import BytesIO, TextIOWrapper


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


def test_direct_types(call_api):
    assert call_api('mul', a=2, b=3) == 6


def test_wrapping(call_api):
    assert call_api('div', a=6, b=2) == 3


def test_literals(call_api):
    list_value = ['a', ['b', 'c'], ['d']]
    dict_value = {'a': ['a', 'b', 'c'], 'b': {'c': {'d': 1, 'e': 2}}}
    rv = call_api('echo', list_value=copy.deepcopy(list_value),
                  dict_value=copy.deepcopy(dict_value))
    assert rv == [list_value, dict_value]


def test_default_to_none(call_api):
    assert call_api('default_to_none', str_value='s') == "Got 's'"
    assert call_api('default_to_none') == "Got None"


def test_no_json_is_bad_request(webapp):
    resp = webapp.post('/default_to_none', raw_response=True)
    assert resp.status_code == codes.bad_request


def test_compressed_api(webapp):
    headers = {'Content-type': 'application/json', 'Content-encoding': 'gzip'}
    data = {'list_value': [1, 2, 3], 'dict_value': {'a': 1, 'b': 2}}
    s = BytesIO()
    with gzip.GzipFile(fileobj=s, mode='wb') as f:
        with TextIOWrapper(f) as w:
            json.dump(data, w)
    compressed = s.getvalue()
    print('compressed: {!r}'.format(compressed))
    resp = webapp.post('/echo', data=compressed, headers=headers)['result']
    assert resp == [data['list_value'], data['dict_value']]
