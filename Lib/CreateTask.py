from TwitterMonitorTask import TwitterMonitorTask

class CreateTask(TwitterMonitorTask):
	"""docstring for CreateTask"""

	info = ''

	def __init__(self, twitter_session, info):
		super(CreateTask, self).__init__()
		self.twitter_session = twitter_session
		self.info = info

	def perform(self):
		print 'CreateTask ', self.info, self.twitter_session
