# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import logging
from subprocess import call
from time import time

from home_brains import Variable


class RecorderPipe(Variable):
    '''
    Records a short audio file from the mic
    '''

    def __init__(self, _id, _param, _inputs=[], _options={}, _trigger_callback=None):
        super(RecorderPipe, self).__init__(_id, _param, _inputs, _options, _trigger_callback)
        self.worker = None

    def process(self):
        '''
        Record 4-second audio file and triggers the circuit manager to process it.
        '''
        filename = "speech-%s.flac" % time()
        cmd = "arecord -f cd -t wav -d 4 -r 16000 | flac - -f -s --best --sample-rate 16000 -o %s" % filename
        logging.debug(cmd)

        code = call(cmd, shell=True)
        if code > 0:
            self.error = True

        self.value = filename

        super(RecorderPipe, self).process()
