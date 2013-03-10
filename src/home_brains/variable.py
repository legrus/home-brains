import logging

class Variable(object):
	"""
	Hold a value, updating it periodically or triggering by events.
	Every other entity is a Variable.
	"""

	value = None
	error = False
	outputs = []

	def __init__(self):
		# TODO: register in a global variable manager
		pass

	def process(self):
		# just nothing, a virtual method
		logging.debug("Processing %s, value = %s %s",
			type(self).__name__,
			self.value,
			("ERROR" if self.error else "")
			)
