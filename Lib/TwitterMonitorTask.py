from Task import Task

class TwitterMonitorTask(Task):
	"""docstring for TwitterMonitorTask"""

	twitter_session = None

	def __init__(self):
		super(TwitterMonitorTask, self).__init__()

	def perform(self):
		raise Exception('TwitterMonitorTask', 'This is an abstract method. Please implement it in your')
