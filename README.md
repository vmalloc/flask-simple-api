
![Build Status] (https://secure.travis-ci.org/vmalloc/flask-simple-api.png )


![Downloads] (https://pypip.in/d/flask-simple-api/badge.png )

![Version] (https://pypip.in/v/flask-simple-api/badge.png )

Overview
========

Flask-Simple-API is a small utility package to create rapid api endpoints using Flask and Python3 annotations:

```python

from flask.ext.simple_api import SimpleAPI

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

You can also pass any arguments that are valid for Flask-Restful's `reqparse` parser through the `ARG` helper:

```python
from flask.ext.simple_api import ARG

@api.include
def do_something_else(value: ARG(type=int, default=6, location='json')):
    ...
```

Licence
=======

BSD3

