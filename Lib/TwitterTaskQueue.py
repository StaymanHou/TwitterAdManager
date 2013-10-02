from MultiTubeQueue import MultiTubeQueue
from CreateTask import CreateTask
from DeleteTask import DeleteTask
import logging

class TwitterTaskQueue(MultiTubeQueue):
	"""docstring for TwitterTaskQueue"""

	in_queue_camp_pk_list = []

	def __init__(self):
		super(TwitterTaskQueue, self).__init__()
		self.in_queue_camp_pk_list = []

	def put(self, tube_name, incoming_item):
		if isinstance(incoming_item, CreateTask) or isinstance(incoming_item, DeleteTask):
			if incoming_item.camp.pk in self.in_queue_camp_pk_list: return
		super(TwitterTaskQueue, self).put(tube_name, incoming_item)

	def open(self, tube_name, incoming_item):
		super(TwitterTaskQueue, self).open(tube_name)
		if isinstance(incoming_item, CreateTask) or isinstance(incoming_item, DeleteTask):
			if incoming_item.camp.pk in self.in_queue_camp_pk_list: self.in_queue_camp_pk_list.remove(incoming_item.camp.pk)


