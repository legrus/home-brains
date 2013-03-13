# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from home_brains import *


class SpeakingPipe(WebSource):
    '''
    Converts text to speech using google translate. Saves its output to a tempfile.
    '''
    #TODO: cache media files

    def create_media_url(self):

        words = self.inputs[0].value
        arg = '+'.join(words.split())
        lang = "en"  # TODO detect language

        return "http://translate.google.com/translate_tts?q=%s&tl=%s" % (arg, lang)

    def process(self):
        super(SpeakingPipe, self).preprocess()  # check inputs are sane

        self.param = self.create_media_url()    # Provide url as param, then run as a WebSource

        super(SpeakingPipe, self).process()

        if not self.error:
            filename = "/tmp/speak-%s.mp3" % self.id

            try:
                # This will create a new file or **overwrite an existing file**.
                f = open(filename, "w")
                try:
                    f.write(self.value)
                finally:
                    f.close()
            except IOError:
                self.error = True

            self.value = filename