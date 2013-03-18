# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import logging
from subprocess import call
from threading import Thread

from home_brains import Variable


class PlaySink(Variable):
    '''
    Plays its input to the default sound device.
    Input: anything playable by mplayer (filename, web stream...)
    '''

    def __init__(self, _id, _param, _inputs=[], _options={}, _trigger_callback=None):
        super(PlaySink, self).__init__(_id, _param, _inputs, _options, _trigger_callback)
        self.worker = None

    def process(self):
        super(PlaySink, self).preprocess()  # check inputs are sane

        if len(self.inputs) == 0 or self.inputs[0].value is None:
            self.error = True
            self.stop()
        else:
            self.value = self.inputs[0].value
            self.play()

        super(PlaySink, self).process()

    def play(self):
        ''' Starts the worker (player) thread in background '''
        self.worker = Thread(target=self._player)
        self.worker.start()

    def stop(self):
        ''' Does not kill the worker thread, but himself dies in attempt '''
        if self.worker is None:
            return

        self.worker.join(1000)
        if self.worker.isAlive():
            raise Exception("Previous speaker not stopped yet!")

    def _player(self):
        cmd = "mplayer -really-quiet %s" % self.value
        logging.debug(cmd)

        code = call(cmd, shell=True)
        if code > 0:
            self.error = True
