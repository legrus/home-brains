# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from subprocess import call
from threading import Thread

from home_brains import *


class FmSink(Variable):
    '''
    Broadcast sound to FM with magnificent PiFM.
    Requires: pifm in $PATH, root permissions (e.g. suid)
    Input: anything playable by ffmpeg (filename, web stream...)
    '''

    def __init__(self, _id, _param, _inputs=[], _options={}):
        super(FmSink, self).__init__(_id, _param, _inputs, _options)
        self.worker = None

    def freq(self):
        ''' Frequency (MHz) for FM transmission '''
        self.get_option("freq") or "102.5"

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
        if self.worker:
            self.stop()
        self.worker = Thread(target=self.player)
        self.worker.start()

    def stop(self):
        self.worker.join(1000)
        if self.worker.isAlive():
            raise Exception("Previous speaker not stopped yet!")

    def player(self):
        cmd = "ffmpeg -i %s -ar 22050 -ac 1 -f wav -acodec pcm_s16le pipe:1 | pifm - %s" % (self.value, self.freq())
        logging.debug(cmd)

        code = call(cmd, shell=True)
        if code > 0:
            self.error = True
