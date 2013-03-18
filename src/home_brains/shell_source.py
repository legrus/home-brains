# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

from subprocess import *
from home_brains import Variable


class ShellSource(Variable):
    '''
    Executes shell command, returning its stdout
    '''

    def cmd(self):
        return self.param  # for ShellSource param is a shell command itself

    def process(self):
        self.error = False

        proc = Popen(self.cmd(), stdout=PIPE, shell=True)
        self.value = proc.stdout.read().rstrip()
        if proc.returncode > 0:
            self.error = True

        # TODO error still does not work!

        super(ShellSource, self).process()
