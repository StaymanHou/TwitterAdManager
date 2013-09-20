from multiprocessing import Process
from time import sleep
import logging
import Config

class TwitterAdMonitor(object):
	"""docstring for TwitterAdMonitor"""

	myprocess = None

	def __init__(self):
		super(TwitterAdMonitor, self).__init__()
		TAMP = Process(target=self.OperateFunction, args=())
		self.myprocess = TAMP

	def start(self):
		self.myprocess.start()

	def join(self):
		self.myprocess.join()

	def OperateFunction():
		config = Config.get()
		logging.info('Controller Process started.')
		# create foreman thread

		# create 
		thread_max_num = config.getint('Monitor', 'worker_thread_max_num')
		if thread_max_num < 1:
			raise Exception('TwitterAdMonitor', 'worker_thread_max_num must be at least 1.')


		#print "'Monitor','b':",config.get('Monitor','b')
		#for i in range(3):
		#	logging.info('This is TAMonitor.')
		#	sleep(1)
	OperateFunction = staticmethod(OperateFunction)