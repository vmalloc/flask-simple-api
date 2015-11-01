from . import simple_api
from .simple_api import error_abort

class SimpleAPI(object):

    def __init__(self, blueprint):
        super(SimpleAPI, self).__init__()
        self._blueprint = blueprint

    def include(self, func):
        return simple_api.api(self._blueprint)(func)
