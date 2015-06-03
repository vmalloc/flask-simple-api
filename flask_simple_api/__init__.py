from .simple_api import api, ARG

class SimpleAPI(object):

    def __init__(self, blueprint):
        super(SimpleAPI, self).__init__()
        self._blueprint = blueprint

    def include(self, func):
        return api(self._blueprint)(func)
