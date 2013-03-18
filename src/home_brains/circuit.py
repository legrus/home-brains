# -*- coding: UTF-8 -*-
# https://github.com/legrus/home-brains, legrus, 2013

import logging

from datetime import datetime, timedelta
from pymongo import MongoClient
from threading import Thread
from time import mktime, sleep

from home_brains import VariableTypes


class Circuit(object):
    '''
    Hold a bunch of variables, updating them periodically or triggering by events.
    '''

    Tick = timedelta(microseconds=1000)

    connection = MongoClient()  # connect to mongo
    db = connection['brains']   # and create/open the database

    def __init__(self, _title="brains"):
        self.title = _title
        self.registry = {}  # hold a link to each registered var here
        self.timeline = {}  # hold a time for all periodical vars here
        self.worker = None  # a worker thread

        self.setup_collection_name = "%s_setup" % self.title  # collection (table) with the variable values
        self.state_collection_name = "%s_state" % self.title  # collection (table) with the variable values

        self.setup_collection = Circuit.db[self.setup_collection_name]
        self.state_collection = Circuit.db[self.state_collection_name]

    def create(self, _type, _id, param, input_names, options):
        if not _type in VariableTypes:
            raise TypeError("Invalid variable type: %s" % _type)

        if _id in self.registry:
            raise NameError("Variable name already exists in this circuit: %s" % _id)

        inputs = [self.find(x) for x in input_names]

        if None in inputs:
            raise NameError("Some of the inputs do not (yet?) exist: %s" % input_names)

        # instantiate variable and register it
        var = VariableTypes[_type](_id, param, inputs, options, self._triggered)
        self.registry[_id] = var

    def start_loop(self):
        logging.debug("Starting loop")
        self.load_state()
        self.save_setup()

        for var in self.registry.values():
            if var.get_option('period'):
                # put all the periodicals into next free slot on the timeline
                self._add_to_timeline(var, datetime.now())

            var.start_background_task()  # for those who have overloaded it

        self.worker = Thread(target=self._loop)
        self.worker.start()
        self.worker.join()

    def _add_to_timeline(self, var, when):
        ''' Tries to schedule var process as close to "when" as possible, with Tick steps. '''

        if var in self.timeline.values():
            # do not add already planned variables
            logging.debug(
                "  not added to timeline(%s): %s already planned/running",
                [var.id for var in self.timeline.values()],
                var.id,
            )
            return

        next_free_tick = when

        while next_free_tick in self.timeline:
            next_free_tick += Circuit.Tick

        self.timeline[next_free_tick] = var

        logging.debug(
            "  added to timeline(%s): %s in %fs (at %s)",
            [var.id for var in self.timeline.values()],
            var.id,
            (next_free_tick-datetime.now()).total_seconds(),
            next_free_tick
        )

    def _remove_from_timeline(self, when):
        del self.timeline[when]

    def _loop(self):

        while True:  # len(self.timeline) > 0:
            now = datetime.now()
            # process all variable due to now

            workload = min(self.timeline.keys()) if len(self.timeline) > 0 else None

            if workload is not None and workload <= now:
                # oops, we're late, go to work
                var = self.timeline[workload]
                logging.debug("Processing '%s'", var.id)
                var.process()
                self._remove_from_timeline(workload)

                if var.get_option('period'):
                    next_process_time = workload + timedelta(seconds=var.get_option('period'))
                    self._add_to_timeline(var, next_process_time)

                # schedule var outputs

                logging.debug("Scheduling '%s' outputs processing(%d)", var.id, len(var.outputs))
                for v in var.outputs:
                    logging.debug("  * %s", v.id)
                    self._add_to_timeline(v, now)

            else:
                self.save_state()
                delay = 1  # (workload - now).total_seconds()
                logging.debug(
                    "No jobs, sleeping for %2.3fs (next job: %s)",
                    delay,
                    self.timeline[workload].id if workload is not None else "None"
                )
                sleep(delay)

    def find(self, var_id):
        ''' Find a variable in the circuit by its name '''
        return self.registry[var_id] if var_id in self.registry else None

    def save_setup(self):
        ''' Save variables setup to the database '''

        logging.debug("Saving setup")

        setup = {
            'timestamp': mktime(datetime.now().timetuple()),
            'circuit': {v.id: v.serialize() for v in self.registry.values()}
        }

        self.setup_collection.insert(setup)

    def save_state(self):
        ''' Save all the variables to the database '''

        state = {
            'timestamp': mktime(datetime.now().timetuple()),
            'circuit': {v.id: v.value_to_save() for v in self.registry.values()}
        }

        self.state_collection.insert(state)

    def load_state(self):
        ''' Load all the variables values from the database '''

        # TODO: put looping variables on the timeline according to the last process time
        # for id, var in self.registry:

        pass

    def _triggered(self, var):
        ''' Called by variables which have triggers in them running in other threads '''

        self._add_to_timeline(var, datetime.now())
