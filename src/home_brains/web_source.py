# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from datetime import datetime
import logging
import urllib2

from home_brains import Variable


class WebSource(Variable):
    '''
    Gets its value from the web. Fetches url given by param or (if it's empty) by first input
    '''

    UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'

    def url(self):
        return self.param  # or len(self.inputs) > 0 and self.inputs[0].value

    def process(self):
        self.error = False
        self.value = None

        if self.param is not None:
            try:
                req = urllib2.Request(self.url(), headers={'User-Agent': WebSource.UserAgent})
                response = urllib2.urlopen(req)
                self.value = response.read()
            except urllib2.HTTPError, e:
                logging.debug("Error: %s", e)
                self.error = True

        if self.value is None:
            self.error = True

        # uncomment to see raw data logged
        # super(WebSource, self).process()

        self.last_processed = datetime.now()

        if self.error:
            logging.debug("Processing WebSource, ERROR")
        else:
            logging.debug("Processing WebSource, len(value) = %s", len(self.value))
