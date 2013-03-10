import logging
from subprocess import *
from home_brainz import *


class ShellInput(Variable):
    """Logical and for its inputs"""
    cmd = ""

    def __init__(self, _cmd):
        self.cmd = _cmd

    def process(self):
        self.error = False

        proc = Popen(self.cmd, stdout = PIPE, shell=True)
        self.value = proc.stdout.read().rstrip()
        if proc.returncode > 0:
            self.error = True

        # TODO error still does not work!

        super(ShellInput, self).process()
