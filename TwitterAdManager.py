from Lib.TwitterAdMonitor import TwitterAdMonitor
from Lib.TwitterAdController import TwitterAdController
import logging
import Lib.Config as Config

class TwitterAdManager(object):
	"""This is the top class of this project. It holds two process: :class:`Lib.TwitterAdMonitor.TwitterAdMonitor` 
	and :class:`Lib.TwitterAdMonitor.TwitterAdMonitor`.
	To start it call :meth:`TwitterAdManager.TwitterAdManager.start`. Call :meth:`TwitterAdManager.TwitterAdManager.join` to wait.
	"""
	
	TAMonitor = None
	"""hold the :class:`Lib.TwitterAdMonitor.TwitterAdMonitor` process."""
	TAController = None
	"""hold the :class:`Lib.TwitterAdController.TwitterAdController` process."""

	def __init__(self):
		super(TwitterAdManager, self).__init__()
		self.TAMonitor = TwitterAdMonitor()
		self.TAController = TwitterAdController()
	
	def start(self):
		"""Start the two processes: :attr:`TwitterAdManager.TwitterAdManager.TAMonitor` 
		process and :attr:`TwitterAdManager.TwitterAdManager.TAController` process.
		"""
		config = Config.get()
		logging.info('TwitterAdManager start')
		self.TAMonitor.start()
		self.TAController.start()

	def stop(self):
		"""Stop the processess if running.(Not implemented yet.)"""
		# TO-DO

	def __del__(self):
		if self.TAMonitor.is_alive():
			self.TAMonitor.terminate()
		if self.TAController.is_alive():
			self.TAController.terminate()

	def join(self):
		"""Wait for the two processes to join."""
		self.TAMonitor.join()
		self.TAController.join()
		logging.info('TwitterAdManager end')


		