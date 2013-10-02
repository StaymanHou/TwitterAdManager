class Task(object):
	"""This is an abstract task class
		with a perform method to be implemented.
	"""

	def __init__(self):
		super(Task, self).__init__()

	def perform(self):
		"""An abstract method to be implemented.
			Usage:

				>>> task = Task()
				>>> task.perform()
		"""
		raise Exception('Task', 'This is an abstract method. Please implement it in your subclass.')
		