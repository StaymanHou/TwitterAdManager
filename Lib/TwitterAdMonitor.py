from multiprocessing import Process
import threading
from Queue import Queue
from time import sleep
import logging
import Config
from TwitterAdForeman import TwitterAdForeman
from TwitterAdWorker import TwitterAdWorker

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
		logging.info('Monitor Process started.')
		# create shared task queue and lock
		TaskQueue = Queue(config.getint('Monitor', 'task_queue_size'))
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