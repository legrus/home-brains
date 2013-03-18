# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from home_brains import Variable
from urllib import urlencode


class VoicePipe(Variable):
    '''
    Converts speech to text using google speech "API".
    '''

    def process(self):
        super(VoicePipe, self).preprocess()  # check inputs are sane

        # TODO

        super(VoicePipe, self).process()
