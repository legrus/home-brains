import logging


class Variable(object):
	"""Hold a value"""
	value = None
	error = False
	sinks = []

	def __init__(self):
		pass

	def process(self):
		# just nothing, a virtual method
		logging.debug("Processing %s, value = %s %s",
			type(self).__name__,
			self.value,
			("ERROR" if self.error else "")
			)

		return
