from Lib.TwitterAdMonitor import TwitterAdMonitor
from Lib.TwitterAdController import TwitterAdController
import logging
import Lib.Config as Config

class TwitterAdManager(object):
	"""docstring for TwitterAdManager"""
	
	TAMonitor = None
	TAController = None

	def __init__(self):
		super(TwitterAdManager, self).__init__()
		self.TAMonitor = TwitterAdMonitor()
		self.TAController = TwitterAdController()
	
	def start(self):
		config = Config.get()
		logging.info('TwitterAdManager start')
		self.TAMonitor.start()
		self.TAController.start()

	def stop(self):
		pass
		# TO-DO

	def __del__(self):
		print 'del called'
		if self.TAMonitor.is_alive():
			self.TAMonitor.terminate()
		if self.TAController.is_alive():
			self.TAController.terminate()

	def join(self):
		self.TAMonitor.join()
		self.TAController.join()
		logging.info('TwitterAdManager end')


		