from multiprocessing import Process
import threading
from TwitterTaskQueue import TwitterTaskQueue
from time import sleep
import logging
import Config
from TwitterAdForeman import TwitterAdForeman
from TwitterAdWorker import TwitterAdWorker

class TwitterAdMonitor(object):
	"""This class operates as a monitor. It keeps updating data between local database 
		and twitter server. Call :meth:`Lib.TwitterAdMonitor.TwitterAdMonitor.start` to start 
		the monitor. The function the process performs is implemented in the static method 
		:meth:`Lib.TwitterAdMonitor.TwitterAdMonitor.OperateFunction`.
	"""

	myprocess = None
	"""hold a :class:`multiprocessing.Process`."""

	def __init__(self):
		super(TwitterAdMonitor, self).__init__()
		TAMP = Process(target=self.OperateFunction, args=())
		self.myprocess = TAMP

	def start(self):
		"""Start the process. Call :meth:`Lib.TwitterAdMonitor.TwitterAdMonitor.myprocess.start`."""
		self.myprocess.start()

	def join(self):
		"""Wait for the process to join. Call :meth:`Lib.TwitterAdMonitor.TwitterAdMonitor.myprocess.join`."""
		self.myprocess.join()

	def is_alive(self):
		"""return a boolean indicates if myprocess is alive"""
		return self.myprocess.is_alive()

	def terminate(self):
		"""Terminate myprocess."""
		self.myprocess.terminate()

	def OperateFunction():
		"""This is a static method. It setups a number of threads including :class:`Lib.TwitterAdForeman.TwitterAdForeman` 
			and :class:`Lib.TwitterAdWorker.TwitterAdWorker` according to the config.ini. 
			You can modify the value of '[Monitor] - worker_thread_max_num'. You must have at least 
			one thread. After the setup, it starts all of the threads, and wait for the threads join.
		"""
		config = Config.get()
		logging.info('Monitor Process started.')
		# create shared task queue and lock
		TaskQueue = TwitterTaskQueue()
		TaskLock = threading.Lock()
		# create empty thread poll
		threads = []
		# create foreman thread
		thread = TwitterAdForeman(TaskQueue, TaskLock)
		threads.append(thread)
		# create worker thread
		thread_max_num = config.getint('Monitor', 'worker_thread_max_num')
		if thread_max_num < 1:
			raise Exception('TwitterAdMonitor', 'worker_thread_max_num must be at least 1.')
		for i in range(thread_max_num):
			thread = TwitterAdWorker(TaskQueue, TaskLock)
			threads.append(thread)
		# start all thread
		for thread in threads:
			thread.start()
		# wait for all threads to complete
		for thread in threads:
			thread.join()
		logging.info('Monitor Process finished.')

	OperateFunction = staticmethod(OperateFunction)