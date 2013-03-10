import logging
from lxml import etree
from home_brainz import *

class XpathPipe(Pipe):
    """Extract value from xml document"""
    xpath = ""

    def __init__(self, _inputs, _xpath):
        super(XpathPipe, self).__init__(_inputs)
        self.xpath = _xpath

    def process(self):
        super(XpathPipe, self).preprocess() # check inputs are sane

        if not self.error:
            doc = etree.XML( self.inputs[0].value )
            self.value = doc.xpath(self.xpath)

        super(XpathPipe, self).process()
