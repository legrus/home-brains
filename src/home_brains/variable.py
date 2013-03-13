# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import logging
from datetime import datetime


class Variable(object):
    '''
    Hold a value, updating it periodically or triggering by events.
    Every other entity is a Variable.
    '''

    def __init__(self, _id, _param, _inputs=[], _options={}):
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

    def serialize(self):
        ''' Not really a cast to string, but to a dictionary '''
        obj = {}
        # save normal attributes
        for key in ['id', 'param', 'options', 'error', 'value']:
            obj[key] = getattr(self, key)

        # save only the ids of inputs and outputs
        for key in ['inputs', 'outputs']:
            obj[key] = [x.id for x in getattr(self, key)]

        return obj

    def value_to_save(self):
        if self.get_option('transient'):
            return None
        else:
            return self.value if not self.error else None

    def process(self):
        ''' A dummy process method to be overriden in the child classes '''
        self.last_processed = datetime.now()

        logging.debug("Processing %s, value = %s %s",
                      type(self).__name__,
                      self.value,
                      "ERROR" if self.error else ""
                      )

    def get_option(self, name):
        return self.options[name] if name in self.options else None

    def preprocess(self):
        ''' If any of the inputs has an error flag, this pipe would also have error on '''

        self.error = False

        for x in self.inputs:
            if x.error:
                self.error = True
