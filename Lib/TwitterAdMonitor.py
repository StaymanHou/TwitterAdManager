from multiprocessing import Process
from time import sleep

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
		for i in range(10):
			print 'This is TAMonitor. ConfPath: ', ConfPath
			sleep(1)
	OperateFunction = staticmethod(OperateFunction)