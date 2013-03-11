# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import logging
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from home_brains import *


class Circuit(object):
    '''
    Hold a bunch of variables, updating them periodically or triggering by events.
    '''

    VariableTypes = {
        "WebSource": WebSource,
        "ShellSource": ShellSource,
        "XpathPipe": XpathPipe,
        "ExpressionPipe": ExpressionPipe,
        "GpioSink": GpioSink
    }

    Tick = timedelta(microseconds = 1000)

    def __init__(self):
        self.registry = {} # hold a link to each registered var here
        self.timeline = {} # hold a time for all periodical vars here
        self.worker = None # a worker thread


    def create(self, _type, _id, param, input_names, options):
        if not _type in Circuit.VariableTypes:
            raise TypeError("Invalid variable type: %s" % _type)

        if _id in self.registry:
            raise NameError("Variable name already exists in this circuit: %s" % _id)

        inputs = [self.find(x) for x in input_names]

        if None in inputs:
            raise NameError("Some of the inputs do not (yet?) exist: %s" % input_names)

        # instantiate variable and register it
        var = Circuit.VariableTypes[_type](_id, param, inputs, options)
        self.registry[_id] = var


    def start_loop(self):
        for var in self.registry.values():
            if 'period' in var.options and not var.options['period'] is None:
                # put all the periodicals into next free slot on the timeline
                self.add_to_timeline(var, datetime.now())

        self.worker = Thread(target = self.loop)
        self.worker.start()
        self.worker.join()


    def add_to_timeline(self, var, when):
        ''' Tries to schedule var process as close to "when" as possible, with Tick steps. '''

        next_free_tick = when

        while next_free_tick in self.timeline:
            next_free_tick += Circuit.Tick

        self.timeline[next_free_tick] = var

        logging.debug("  added to timeline(%d): %s in %fs (at %s)",
            len(self.timeline.keys()),
            var.id,
            (next_free_tick-datetime.now()).total_seconds(),
            next_free_tick
        )

    def remove_from_timeline(self, when):
        del self.timeline[when]


    def loop(self):

        while len(self.timeline) > 0:
            now = datetime.now()
            # process all variable due to now

            workload = min(self.timeline.keys())

            if workload <= now:
                # oops, we're late, go to work
                var = self.timeline[workload]
                logging.debug("Processing '%s'", var.id)
                var.process()
                self.remove_from_timeline(workload)

                if 'period' in var.options and not var.options['period'] is None:
                    next_process_time = workload + timedelta(seconds = var.options['period'])
                    self.add_to_timeline(var, next_process_time)

                # schedule var outputs

                logging.debug("Scheduling '%s' outputs processing(%d)", var.id, len(var.outputs))
                for v in var.outputs:
                    logging.debug("  * %s", v.id)
                    self.add_to_timeline(v, now)

            else:
                delay = (workload - now).total_seconds()
                logging.debug("No jobs, sleeping for %fs (next job: %s)", delay, self.timeline[workload].id)
                sleep(delay)

    def find(self, var_id):
        ''' Find a variable in the circuit by name '''
        return self.registry[var_id] if var_id in self.registry else None
