class Task(object):
	"""docstring for Task
	   This is an abstract class
	   with a perform method to be implemented
	"""

	def __init__(self):
		super(Task, self).__init__()

	def perform(self):
		raise Exception('Task', 'This is an abstract method. Please implement it in your subclass.')
		