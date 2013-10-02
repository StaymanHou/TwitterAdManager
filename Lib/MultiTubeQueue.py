from Queue import Queue
import logging

class MultiTubeQueue(object):
	"""docstring for MultiTubeQueue"""

	Queues = {}
	pointer = 0

	def __init__(self):
		super(MultiTubeQueue, self).__init__()
		self.Queues = {}
		self.pointer = 0

	def add_tube(self, tube_name):
		if tube_name in self.Queues:
			raise Exception('MultiTubeQueue', 'tube_name already exists')
		self.Queues[tube_name] = {'open': True, 'queue': Queue()}

	def remove_tube(self, tube_name):
		if tube_name not in self.Queues:
			raise Exception('MultiTubeQueue', 'tube_name does not exist')
		del self.Queues[tube_name]
			
	def put(self, tube_name, incoming_item):
		if tube_name not in self.Queues:
			raise Exception('MultiTubeQueue', 'tube_name does not exist')
		self.Queues[tube_name]['queue'].put(incoming_item)

	def get(self):
		for i in range(len(self.Queues)):
			tube_name = self.Queues.keys()[self.pointer]
			item = self.Queues[tube_name]
			if item['open'] and not item['queue'].empty():
				self.close(tube_name)
				return tube_name, item['queue'].get()
			self.next()
		raise Exception('MultiTubeQueue', "can't get. check no_get before get.")

	def close(self, tube_name):
		self.Queues[tube_name]['open'] = False

	def open(self, tube_name):
		if tube_name not in self.Queues:
			logging.warning('Can\'t open a non-existing tube.')
			return
		self.Queues[tube_name]['open'] = True

	def no_get(self):
		flag = True
		for queue in [item['queue'] for item in self.Queues.values() if item['open']]:
			if not queue.empty():
				flag = False
				break
		return flag

	def next(self):
		self.pointer += 1
		if self.pointer >= len(self.Queues):
			self.pointer -= len(self.Queues)
