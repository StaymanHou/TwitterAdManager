from LocalUpdateTask import LocalUpdateTask
from DeleteTask import DeleteTask
from CreateTask import CreateTask

class TaskFactory(object):
	"""docstring for TaskFactory"""

	twitter_session = None

	def __init__(self, twitter_session):
		super(TaskFactory, self).__init__()
		self.twitter_session = twitter_session

	def get_delete_tasks(self):
		"""returns deletetasks as a list of tasks. if no new
		   task return a empty list.
		"""
		return [DeleteTask(self.twitter_session, 1), DeleteTask(self.twitter_session, 2)]

	def get_create_tasks(self):
		return [CreateTask(self.twitter_session, 'a'), CreateTask(self.twitter_session, 'b')]

	def get_local_update_task(self):
		"""returns one task. not a list
		"""
		return LocalUpdateTask(self.twitter_session, 921)
