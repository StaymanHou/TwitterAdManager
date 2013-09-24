from TwitterMonitorTask import TwitterMonitorTask

class CreateTask(TwitterMonitorTask):
	"""docstring for CreateTask"""

	camp = None

	def __init__(self, twitter_session, camp):
		super(CreateTask, self).__init__()
		self.twitter_session = twitter_session
		self.camp = camp

	def perform(self):
		print 'CreateTask ', self.camp.__dict__, self.twitter_session.account.__dict__
