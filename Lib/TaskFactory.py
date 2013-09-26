from LocalUpdateTask import LocalUpdateTask
from DeleteTask import DeleteTask
from CreateTask import CreateTask
from TwitterCampaign import TwitterCampaign
from LocalStatus import LocalStatus

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
		camp_list = TwitterCampaign.get_list(self.twitter_session.account.fi_id, local_status=LocalStatus.TitletoPK['DeletePending'])
		task_list = []
		for camp in camp_list:
			task_list.append(DeleteTask(self.twitter_session, camp))
		return task_list

	def get_create_tasks(self):
		camp_list = TwitterCampaign.get_list(self.twitter_session.account.fi_id, local_status=LocalStatus.TitletoPK['CreatePending'])
		task_list = []
		for camp in camp_list:
			task_list.append(CreateTask(self.twitter_session, camp))
		return task_list

	def get_local_update_task(self, hour_start=None):
		"""returns one task. not a list
		"""
		return LocalUpdateTask(self.twitter_session, 921)
