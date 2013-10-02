from MultiTubeQueue import MultiTubeQueue
from CreateTask import CreateTask
from DeleteTask import DeleteTask
import logging

class TwitterTaskQueue(MultiTubeQueue):
	"""Specific Queue for orginizing twitter tasks. 
		It keeps track of task.camp pks within the queue, so that 
		each campaign will only be involve in one task simultaneously.
	"""

	in_queue_camp_pk_list = []

	def __init__(self):
		super(TwitterTaskQueue, self).__init__()
		self.in_queue_camp_pk_list = []

	def put(self, tube_name, incoming_item):
		"""Check the pk of incoming_item.
		"""
		if isinstance(incoming_item, CreateTask) or isinstance(incoming_item, DeleteTask):
			if incoming_item.camp.pk in self.in_queue_camp_pk_list: return
			self.in_queue_camp_pk_list.append(incoming_item.camp.pk)
		super(TwitterTaskQueue, self).put(tube_name, incoming_item)

	def open(self, tube_name, incoming_item):
		super(TwitterTaskQueue, self).open(tube_name)
		if isinstance(incoming_item, CreateTask) or isinstance(incoming_item, DeleteTask):
			if incoming_item.camp.pk in self.in_queue_camp_pk_list: self.in_queue_camp_pk_list.remove(incoming_item.camp.pk)


