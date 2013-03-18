# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from home_brains import Variable


class ExpressionPipe(Variable):
    """ Evaluates arbitrary expression like "{0} > {1}" over its inputs """

    def expr(self):
        return self.param  # param is an xpath expression for XPathPipe

    def process(self):
        super(ExpressionPipe, self).preprocess()

        if not self.error:
            # get input values in a list
            args = map(lambda x: int(x.value), self.inputs)

            # Yes I know eval is evil.
            # But I control expr and args are restricted to integers.
            self.value = eval(self.expr().format(*args))

        super(ExpressionPipe, self).process()
