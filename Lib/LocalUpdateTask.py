from TwitterMonitorTask import TwitterMonitorTask

class LocalUpdateTask(TwitterMonitorTask):
	"""docstring for LocalUpdateTask"""

	time = 920

	def __init__(self, twitter_session, time):
		super(LocalUpdateTask, self).__init__()
		self.twitter_session = twitter_session
		self.time = time

	def perform(self):
		print 'LocalUpdateTask ', self.time, self.twitter_session