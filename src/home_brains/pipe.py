import logging
from home_brains import *


class Pipe(Variable):
    """
    Perform operations on input variables when processed.
    """

    inputs = []

    def __init__(self, _inputs):
        self.inputs = []
        for x in _inputs:
            if isinstance(x, Variable):
                self.inputs.append(x)
                x.outputs.append(self)

        logging.debug("Pipe.__init__: inputs = %s", self.inputs)
        super(Pipe, self).__init__()

    def preprocess(self):
        """ If any of the inputs has an error flag, this pipe would also have error on """

        self.error = False

        for x in self.inputs:
            if x.error:
                self.error = True

    def process(self):
        super(Pipe, self).process()
