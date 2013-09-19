from multiprocessing import Process
from time import sleep
import logging
import Config

class TwitterAdController(object):
	"""docstring for TwitterAdController"""

	myprocess = None

	def __init__(self, ConfPath):
		super(TwitterAdController, self).__init__()
		TACP = Process(target=self.OperateFunction, args=(ConfPath,))
		self.myprocess = TACP

	def start(self):
		self.myprocess.start()

	def join(self):
		self.myprocess.join()

	def OperateFunction(ConfPath):
		config = Config.get()
		print "'Controller','c':",config.get('Controller','c')

		for i in range(3):
			logging.info('This is TAController. ConfPath: '+ConfPath)
			sleep(1)
	OperateFunction = staticmethod(OperateFunction)