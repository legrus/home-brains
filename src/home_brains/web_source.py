# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import urllib2
from home_brains import *


class WebSource(Variable):
    """ Gets its value from the web """

    url = ""

    def __init__(self, _url):
        self.url = _url

    def process(self):
        self.error = False
        try:
            response = urllib2.urlopen(self.url)
            self.value = response.read()
        except urllib2.HTTPError:
            # TODO never goes here; fix
            self.error = True

        if self.value is None:
            self.error = True

        # uncomment to see raw data logged
        # super(WebSource, self).process()

        if self.error:
            logging.debug("Processing WebSource, ERROR")
        else:
            logging.debug("Processing WebSource, len(value) = %s", len(self.value))
