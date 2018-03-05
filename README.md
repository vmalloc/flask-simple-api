
![Build Status](https://secure.travis-ci.org/vmalloc/flask-simple-api.png)
![Version](https://img.shields.io/pypi/v/flask-simple-api.svg)

Overview
========

Flask-Simple-API is a small utility package to create rapid api endpoints using Flask and Python3 annotations:

```python

from flask_simple_api import SimpleAPI

app = Flask(__name__)

api = SimpleAPI(app)

@api.include
def do_something(param1: int, param2: str):
    return 'String is {}, and number is {}'.format(param1, param2)

```

Flask-Simple-API serializes the return value to JSON. For example the above would yield the following:

```
curlish -X POST http://your.server.name/do_something -J param1:=2 -J param2=hello

{"result": "String is hello, and number is 2"}
```

Optional and default values:

```python
@api.include
def do_something_else(value: int=2, value: str=None):
    ...
```

Licence
=======

BSD3

