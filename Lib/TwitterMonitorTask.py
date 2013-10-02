from Task import Task

class TwitterMonitorTask(Task):
	"""Abstract Task class for TwitterMonitor. Have to hold a reference of 
		:class:`Lib.TwitterSession`.
	"""

	twitter_session = None

	def __init__(self):
		super(TwitterMonitorTask, self).__init__()

	def perform(self):
		"""This is an abstract method. Have to be implemented in sub classes.
			Inherite from :func:`Lib.Task.Task.perform`.
		"""
		raise Exception('TwitterMonitorTask', 'This is an abstract method. Please implement it in your')
