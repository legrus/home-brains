# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import logging
from home_brains import *


class Pipe(Variable):
    """
    Perform operations on input variables when processed.
    """

    def preprocess(self):
        """ If any of the inputs has an error flag, this pipe would also have error on """

        self.error = False

        for x in self.inputs:
            if x.error:
                self.error = True

    def process(self):
        super(Pipe, self).process()
