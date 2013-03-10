import logging
from home_brainz import *


class Pipe(Variable):
    """Join or operate on variables"""
    inputs = []

    def __init__(self, _inputs):
        self.inputs = []
        for x in _inputs:
            if isinstance(x, Variable):
                self.inputs.append(x)
                x.sinks.append(self)

        logging.debug("Pipe.__init__: inputs = %s", self.inputs)
        super(Pipe, self).__init__()

    def preprocess(self):
        self.error = False

        for x in self.inputs:
            if x.error:
                self.error = True

    def process(self):
        super(Pipe, self).process()
