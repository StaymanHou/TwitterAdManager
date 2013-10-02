from Queue import Queue
import logging

class MultiTubeQueue(object):
	"""This is a collection of queues. The queue inside this class is called tube.
		Each tube has a specific name. Tubes can be added and removed by its name 
		by calling :func:`Lib.MultiTubeQueue.MultiTubeQueue.add_tube` and 
		:func:`Lib.MultiTubeQueue.MultiTubeQueue.remove_tube`.
		For producer, it can put items to specified tube by calling 
		:func:`Lib.MultiTubeQueue.MultiTubeQueue.put`.
		For consumer, it is an integral queue, can get items from it by calling 
		:func:`Lib.MultiTubeQueue.MultiTubeQueue.get`. Upon get() is called, the corresponding 
		tube will be closed, and return both the name of the tube and the item.
		You have to open the tube to make getable again by calling 
		:func:`Lib.MultiTubeQueue.MultiTubeQueue.open`.
		**Always** check :func:`Lib.MultiTubeQueue.MultiTubeQueue.no_get` before get().

			>>> mtq = MultiTubeQueue()
			>>> ...
			>>> if not mtq.no_get():
			>>>     tubename, item = mtq.get()

		MultiTubeQueue will keep circling the tubes, and give out the item which is first getable.
	"""

	Queues = {}
	pointer = 0

	def __init__(self):
		super(MultiTubeQueue, self).__init__()
		self.Queues = {}
		self.pointer = 0

	def add_tube(self, tube_name):
		"""Add a tube with the tube_name provided into this queue. 
			Initially, the status of the new tube is open.
		"""
		if tube_name in self.Queues:
			raise Exception('MultiTubeQueue', 'tube_name already exists')
		self.Queues[tube_name] = {'open': True, 'queue': Queue()}

	def remove_tube(self, tube_name):
		"""Remove a tube with the given tube_name.
			The items in the tube will also be discarded.
		"""
		if tube_name not in self.Queues:
			raise Exception('MultiTubeQueue', 'tube_name does not exist')
		del self.Queues[tube_name]
			
	def put(self, tube_name, incoming_item):
		"""Put an item into the tube with the given tube_name.
			If tube_name is not exist, Exception will be raised.
		"""
		if tube_name not in self.Queues:
			raise Exception('MultiTubeQueue', 'tube_name does not exist')
		self.Queues[tube_name]['queue'].put(incoming_item)

	def get(self):
		"""Get an item from the queue. The corresponding tube will be 
			closed after a item is got.
		"""
		for i in range(len(self.Queues)):
			tube_name = self.Queues.keys()[self.pointer]
			item = self.Queues[tube_name]
			if item['open'] and not item['queue'].empty():
				self.close(tube_name)
				return tube_name, item['queue'].get()
			self.next()
		raise Exception('MultiTubeQueue', "can't get. check no_get before get.")

	def close(self, tube_name):
		"""Close the tube with the given tube_name.
		"""
		self.Queues[tube_name]['open'] = False

	def open(self, tube_name):
		"""Open the tube with the given tube_name.
		"""
		if tube_name not in self.Queues:
			logging.warning('Can\'t open a non-existing tube.')
			return
		self.Queues[tube_name]['open'] = True

	def no_get(self):
		"""Return True if there is something getable in any tube. False 
			if there's non.
		"""
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
