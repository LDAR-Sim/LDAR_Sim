import time
from functools import wraps


def timer(method):
    @wraps(method)
    def timed(self, *args, **kwargs):
        ts = time.time()
        result = method(self, *args, **kwargs)
        te = time.time()
        try:
            self.state['perform_test'][method.__name__] += te - ts
        except KeyError:
            self.state['perform_test'].update({method.__name__: te - ts})
        return result
    return timed
