class Task(object):
	"""docstring for Task"""

	name = None
	id = None

	def __init__(self, name, id):
		super(Task, self).__init__()
		self.name = name
		self.id = id

	def perform(self):
		print 'Task #', self.id, ' performed for session ', self.name
		