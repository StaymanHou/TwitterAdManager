from TwitterMonitorTask import TwitterMonitorTask

class DeleteTask(TwitterMonitorTask):
	"""docstring for DeleteTask"""

	id = 0

	def __init__(self, twitter_session, id):
		super(DeleteTask, self).__init__()
		self.twitter_session = twitter_session
		self.id = id

	def perform(self):
		print 'DeleteTask ', self.id, self.twitter_session