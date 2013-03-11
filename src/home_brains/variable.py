# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import logging
from datetime import datetime

class Variable(object):
    '''
    Hold a value, updating it periodically or triggering by events.
    Every other entity is a Variable.
    '''

    def __init__(self, _id, _param, _inputs = [], _options = {}):
        (self.id, self.param, self.options) = (_id, _param, _options)

        self.inputs = []
        self.outputs = []
        self.error = False
        self.value = None

        for x in _inputs:
            if not isinstance(x, Variable):
                raise TypeError("Pipe source must be a Variable")

            self.inputs.append(x)
            x.outputs.append(self)

        logging.debug("Created %s, param = '%s', inputs = %s",
            type(self).__name__,
            _param,
            [x.id for x in self.inputs]
        )

    def process(self):
        self.last_processed = datetime.now()

        logging.debug("Processing %s, value = %s %s",
            type(self).__name__,
            self.value,
            "ERROR" if self.error else ""
        )
