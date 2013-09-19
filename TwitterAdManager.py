from Lib.TwitterAdMonitor import TwitterAdMonitor
from Lib.TwitterAdController import TwitterAdController

class TwitterAdManager(object):
	"""docstring for TwitterAdManager"""
	
	ConfPath = None
	TAMonitor = None
	TAController = None

	def __init__(self, ConfPath):
		super(TwitterAdManager, self).__init__()
		if ConfPath is None:
			raise Exception('ConfPath not given.')		
		self.ConfPath = ConfPath
		self.TAMonitor = TwitterAdMonitor(self.ConfPath)
		self.TAController = TwitterAdController(self.ConfPath)
	
	def start(self):
		print 'TwitterAdManager start'
		self.TAMonitor.start()
		self.TAController.start()

	def stop(self):
		pass
		# TO-DO

	def join(self):
		self.TAMonitor.join()
		self.TAController.join()
		print 'TwitterAdManager end'


		