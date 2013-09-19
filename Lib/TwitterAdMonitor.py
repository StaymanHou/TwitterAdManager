from multiprocessing import Process
from time import sleep
import logging
import Config

class TwitterAdMonitor(object):
	"""docstring for TwitterAdMonitor"""

	myprocess = None

	def __init__(self, ConfPath):
		super(TwitterAdMonitor, self).__init__()
		TAMP = Process(target=self.OperateFunction, args=(ConfPath,))
		self.myprocess = TAMP

	def start(self):
		self.myprocess.start()

	def join(self):
		self.myprocess.join()

	def OperateFunction(ConfPath):
		config = Config.get()
		print "'Monitor','b':",config.get('Monitor','b')
		for i in range(3):
			logging.info('This is TAMonitor. ConfPath: '+ConfPath)
			sleep(1)
	OperateFunction = staticmethod(OperateFunction)