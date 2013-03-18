# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import json
import logging
import urllib2

from home_brains import Variable


class VoicePipe(Variable):
    '''
    Converts speech to text using google speech "API".
    '''

    def process(self):
        super(VoicePipe, self).preprocess()  # check inputs are sane

        # TODO
        # working cmdline:
        # wget --post-file out.flac
        #   --header="Content-Type: audio/x-flac; rate=16000"
        #   -O speech.txt
        #   http://www.google.com/speech-api/v1/recognize?lang=ru

        self.error = False
        self.value = None

        if len(self.inputs) > 0:
            filename = self.inputs[0].value

            try:
                lang = 'ru'
                url = 'http://www.google.com/speech-api/v1/recognize?lang=%s' % lang
                header = {'Content-Type': 'audio/x-flac; rate=16000"'}
                flac = open(filename, 'rb').read()
                req = urllib2.Request(url, flac, header)
                response = urllib2.urlopen(req).read().decode('utf-8')
                speech = json.loads(response)

                logging.debug(" * Google speech response: %s", speech)

                if 'status' in speech and speech['status'] == 0:
                    self.value = speech['hypotheses'][0]['utterance'].encode('utf-8')

            except urllib2.HTTPError, e:
                logging.debug("Error: %s", e)
                self.error = True
            except ValueError, e:
                logging.debug("Error: %s", e)
                self.error = True

        if self.value is None:
            self.error = True

        super(VoicePipe, self).process()
