from multiprocessing import Process
from time import sleep

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
		for i in range(10):
			print 'This is TAController. ConfPath: ', ConfPath
			sleep(1)
	OperateFunction = staticmethod(OperateFunction)