# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from home_brains import Variable
import re


class RegexpPipe(Variable):
    '''
    Extract first match from the text with a regular expression.
    Regular expression flags can be passed to 're' option:
        RegexpPipe('extract_first_word', '^(\s+)', ['some_other_var'], {'re':re.UNICODE})
    '''

    def regexp(self):
        return self.param  # param is an regular expression for RegexpSink

    def flags(self):
        return self.get_option("re") or 0

    def process(self):
        super(RegexpPipe, self).preprocess()  # check inputs are sane

        if not self.error:
            self.value = re.search(
                self.regexp(),
                self.inputs[0].value,
                self.flags()
            ).group(1)

        super(RegexpPipe, self).process()
