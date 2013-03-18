# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import logging
from subprocess import call
from threading import Thread

from home_brains import Variable


class FmSink(Variable):
    '''
    Broadcast sound to FM with magnificent PiFM.
    Requires: pifm in $PATH, root permissions for it (e.g. suid)
    Input: anything playable by ffmpeg (filename, web stream...)
    '''

    def __init__(self, _id, _param, _inputs=[], _options={}, _trigger_callback=None):
        super(FmSink, self).__init__(_id, _param, _inputs, _options, _trigger_callback)
        self.worker = None

    def freq(self):
        ''' Frequency (MHz) for FM transmission '''
        return self.param

    def process(self):
        super(FmSink, self).preprocess()  # check inputs are sane

        if len(self.inputs) == 0 or self.inputs[0].value is None:
            self.error = True
            self.stop()
        else:
            self.value = self.inputs[0].value
            self.play()

        super(FmSink, self).process()

    def play(self):
        ''' Starts the worker (broadcasting) thread in background '''
        if self.worker:
            self.stop()
        self.worker = Thread(target=self.player)
        self.worker.start()

    def stop(self):
        ''' Does not kill the thread, but himself dies in attempt '''
        self.worker.join(1000)
        if self.worker.isAlive():
            # TODO: kill pifm here
            raise Exception("Previous speaker not stopped yet!")

    def player(self):
        cmd = "avconv -i %s -ar 22050 -ac 1 -f wav -acodec pcm_s16le pipe:1 | pifm - %s" % (self.value, self.freq())
        logging.debug(cmd)

        code = call(cmd, shell=True)
        if code > 0:
            self.error = True
