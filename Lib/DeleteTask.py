from TwitterMonitorTask import TwitterMonitorTask

class DeleteTask(TwitterMonitorTask):
	"""docstring for DeleteTask"""

	camp = None

	def __init__(self, twitter_session, camp):
		super(DeleteTask, self).__init__()
		self.twitter_session = twitter_session
		self.camp = camp

	def perform(self):
		print 'DeleteTask ', self.camp.__dict__, self.twitter_session.account.__dict__