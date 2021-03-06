# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from home_brains import Variable


class AndPipe(Variable):
    '''Logical AND for its inputs'''

    def process(self):
        super(AndPipe, self).preprocess()

        if not self.error:
            self.value = True

            for x in self.inputs:
                xx = 0
                try:
                    xx = int(x.value)
                except ValueError:
                    pass

                self.value = self.value and xx

        super(AndPipe, self).process()

