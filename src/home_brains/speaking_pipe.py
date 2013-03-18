# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from home_brains import WebSource
import logging
from urllib import urlencode
from guess_language import guessLanguageTag


class SpeakingPipe(WebSource):
    '''
    Converts text to speech using google translate. Saves its output to a tempfile.
    '''
    #TODO: cache media files

    def detect_language(self):
        lang_from_options = self.get_option('lang')

        text_for_guess_lang = ((self.inputs[0].value or " ") + " ") * 5  # this library handles long texts better somehow
        guessed_lang = guessLanguageTag(text_for_guess_lang)
        if guessed_lang == 'UNKNOWN':
            guessed_lang = None

        logging.debug(" * detect_language: %s %s %s ", lang_from_options, guessed_lang, 'en')
        return lang_from_options or guessed_lang or 'en'

    def create_media_url(self):
        if self.inputs[0].value is None:
            return None

        lang = self.detect_language()

        logging.debug(" * ok, val=%s, lang=%s", self.inputs[0].value, lang)

        query = urlencode({
            'q': self.inputs[0].value,
            'tl': lang
        })

        return 'http://translate.google.com/translate_tts?%s' % query

    def process(self):
        super(SpeakingPipe, self).preprocess()  # check inputs are sane

        self.param = self.create_media_url()    # Provide url as param, then run as a WebSource

        super(SpeakingPipe, self).process()

        if not self.error:
            filename = "/tmp/speak-%s.mp3" % self.id

            try:
                f = open(filename, "w")
                try:
                    f.write(self.value)
                finally:
                    f.close()
            except IOError:
                self.error = True

            self.value = filename
