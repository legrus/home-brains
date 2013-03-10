import logging
from home_brains import *


class AndPipe(Pipe):
    """Logical AND for its inputs"""

    def __init__(self, _inputs):
        super(AndPipe, self).__init__(_inputs)

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

