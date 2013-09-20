from multiprocessing import Process
from time import sleep
import logging
import Config

class TwitterAdController(object):
	"""docstring for TwitterAdController"""

	myprocess = None

	def __init__(self):
		super(TwitterAdController, self).__init__()
		TACP = Process(target=self.OperateFunction, args=())
		self.myprocess = TACP

	def start(self):
		self.myprocess.start()

	def join(self):
		self.myprocess.join()

	def OperateFunction():
		config = Config.get()
		for i in range(3):
			logging.info('This is TAController')
			sleep(1)
	OperateFunction = staticmethod(OperateFunction)