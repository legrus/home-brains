# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import logging
from lxml import etree
from home_brains import *

class XpathPipe(Pipe):
    """Extract value from xml document"""

    def xpath(self):
        return self.param # param is an xpath expression for XPathPipe

    def process(self):
        super(XpathPipe, self).preprocess() # check inputs are sane

        if not self.error:
            doc = etree.XML( self.inputs[0].value )
            self.value = doc.xpath(self.xpath())

        super(XpathPipe, self).process()
