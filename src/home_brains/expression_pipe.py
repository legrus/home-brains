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
            # get input values in a list
            args = map(lambda x: int(x.value), self.inputs)

            # yes I know eval is evil.
            # but i control expr, and supply it with user input restricted to integers.
            self.value = eval ( self.expr.format(*args) )

        super(ExpressionPipe, self).process()
