from TwitterMonitorTask import TwitterMonitorTask
import logging
import re

class LocalUpdateTask(TwitterMonitorTask):
	"""docstring for LocalUpdateTask"""

	twitter_session = None
	hour_start = None

	def __init__(self, twitter_session, hour_start):
		super(LocalUpdateTask, self).__init__()
		self.twitter_session = twitter_session
		self.hour_start = hour_start

	def perform(self):
		print 'LocalUpdateTask ', self.time, self.twitter_session