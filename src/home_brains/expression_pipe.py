import logging
from home_brains import *


class ExpressionPipe(Pipe):
    """ Evaluates arbitrary expression like "{0} > {1}" over its inputs """

    expr = "0"

    def __init__(self, _inputs, _expr):
        self.expr = _expr
        super(ExpressionPipe, self).__init__(_inputs)

    def process(self):
        super(ExpressionPipe, self).preprocess()

        if not self.error:
            args = map(lambda x: x.value, self.inputs) # get input values in a list
            self.value = eval ( self.expr.format(*args) )   # yes I know eval is evil

        super(ExpressionPipe, self).process()
