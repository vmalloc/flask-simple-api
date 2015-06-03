from . import simple_api

class SimpleAPI(object):

    def __init__(self, blueprint):
        super(SimpleAPI, self).__init__()
        self._blueprint = blueprint

    def include(self, func):
        return simple_api.api(self._blueprint)(func)
