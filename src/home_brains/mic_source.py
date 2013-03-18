# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import audioop
import logging
import pyaudio
from threading import Thread

from home_brains import Variable


class MicSource(Variable):
    '''
    Waits for the predefined sound pattern on the mic
    '''

    def __init__(self, _id, _param, _inputs=[], _options={}, _trigger_callback=None):
        super(MicSource, self).__init__(_id, _param, _inputs, _options, _trigger_callback)
        self.worker = None

    def process(self):
        # do nothing, all the processing was done in the worker thread.
        # just save the value and let the circuit manager precess the
        # downstream variables.
        super(MicSource, self).process()

    def start_background_task(self):
        ''' Starts the worker (listening) thread in background '''
        self.worker = Thread(target=self._listen)
        self.worker.start()

    def _listen(self):
        '''
        This method runs in background.
        Each time it detects acoustic trigger (wait_for_claps), it records a
        4-second audio file and triggers the circuit manager to process it.
        '''
        while True:
            self._wait_for_claps()
            self.error = False
            self.value = True

            if self.trigger_callback is not None:
                self.trigger_callback(self)

    def _wait_for_claps(self):
        ''' Listens to mic until there is a clap, followed by silence, then another clap '''
        CHUNK = 1600
        CHANNELS = 1  # mono
        RATE = 16000  # sampling freq, Hz
        WINDOW = 10
        last_records = [0] * WINDOW

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,  # 16-bit
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        logging.debug("* listening")

        last_peak = 0
        trigger = False
        n_chunk = 0

        while not trigger:
            n_chunk += 1
            data = stream.read(CHUNK)
            rms = audioop.rms(data, CHANNELS*2)  # 2 for bytes per sample

            last_records[n_chunk % WINDOW] = rms

            avg = sum(last_records) / WINDOW

            is_peak = n_chunk > WINDOW and rms > 4 * avg

            if is_peak:
                if last_peak == 0:
                    last_peak = n_chunk  # first clap
                else:
                    if n_chunk - last_peak > 1:
                        trigger = True
            else:
                if last_peak > 0 and n_chunk - last_peak > 5:
                    last_peak = 0  # forget everything after 1 second
