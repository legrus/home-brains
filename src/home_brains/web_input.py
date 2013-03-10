import urllib2
from home_brains import *


class WebInput(Variable):
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
        # super(WebInput, self).process()

        if self.error:
            logging.debug("Processing WebInput, ERROR")
        else:
            logging.debug("Processing WebInput, len(value) = %s", len(self.value))

        return
