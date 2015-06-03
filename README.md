
![Build Status] (https://secure.travis-ci.org/vmalloc/flask-simple-api.png )


![Downloads] (https://pypip.in/d/flask-simple-api/badge.png )

![Version] (https://pypip.in/v/flask-simple-api/badge.png )

Overview
========

Flask-Simple-API is a small utility package to create rapid api endpoints using Flask and Python3 annotations:

```python

from flask.ext.simple_api import api, ARG

app = Flask(__name__)

@api(app)
def do_something(param1: ARG(type=int, default=0), param2: ARG(type=str)):
    return 'String is {}, and number is {}'.format(param1, param2)

```

Flask-Simple-API serializes the return value to JSON. For example the above would yield the following:

```
curlish -X POST http://your.server.name/do_something -J param1:=2 -J param2=hello

{"result": "String is hello, and number is 2"}
```

Licence
=======

BSD3

