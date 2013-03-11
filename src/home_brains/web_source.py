# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from datetime import datetime
from urllib2 import urlopen

from home_brains import *


class WebSource(Variable):
    '''
    Gets its value from the web
    '''

    def url(self):
        return self.param # for ShellSource param is a shell command itself

    def process(self):
        self.error = False
        try:
            response = urlopen(self.url())
            self.value = response.read()
        except urllib2.HTTPError:
            # TODO never goes here; fix
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
