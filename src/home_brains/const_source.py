# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from home_brains import *


class ConstSource(Variable):
    '''
    Evaluates to a constant
    '''

    def process(self):
        self.error = False
        self.value = self.param

        super(ConstSource, self).process()
