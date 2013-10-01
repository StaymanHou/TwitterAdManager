import threading
import logging
import Config
from time import sleep
from MultiTubeQueue import MultiTubeQueue
import SessionHelper
import TaskHelper

class TwitterAdWorker(threading.Thread):
    """Worker extends :class:`threading.Thread`. After starting, 
        it will periodically check the :attr:`TaskQueue`. If there are works 
        fetchable, and fetch and work on the task. Upon finishing the task, 
        it opens the corresponding tube of the :attr:`TaskQueue`.
    """
    
    config = None
    CheckInterval = 0
    LoadInterval = 0
    TaskQueue = None
    """It is responsible for the communication between :class:`Lib.TwitterAdForeman.TwitterAdForeman` 
        thread and :class:`Lib.TwitterAdWorker.TwitterAdWorker`  threads. It is an object of 
        :class:`Lib.MultiTubeQueue.MultiTubeQueue`.
    """
    TaskLock = None

    def __init__(self, TaskQueue, TaskLock):
        super(TwitterAdWorker, self).__init__()
        self.TaskQueue = TaskQueue
        self.TaskLock = TaskLock
        self.config = Config.get()
        self.CheckInterval = self.config.getint('Monitor_Worker', 'check_interval_in_sec')
        if self.CheckInterval < 1:
            raise Exception('TwitterAdWorker', 'check_interval_in_sec must be at least 1.')
        self.LoadInterval = self.config.getint('General', 'load_interval')
        if self.LoadInterval < 0:
            raise Exception('TwitterAdWorker', 'load_interval must be at least 0.')

    def run(self):
        """Implement the interface of Thread. it Periodically calls 
            :meth:`Lib.TwitterAdWorker.TwitterAdWorker.check`.
        """
        logging.info('TwitterAdWorker thread started')
        while 1:
            sleep(self.CheckInterval)
            self.check()
        logging.info('TwitterAdWorker thread finished')

    def check(self):
        """Loop until no task to do. Within the loop, it checks the :attr:`TaskQueue`.
            If get a task, it calls :meth:`Lib.Task.Task.perform` of the task. Upon finishing the task, 
            it opens the corresponding tube so that no two works will work on the tasks of a same 
            account simultaneously.
        """
        while 1:
            self.TaskLock.acquire()
            if self.TaskQueue.no_get():
                self.TaskLock.release()
                break
            else:
                tube_name, task = self.TaskQueue.get()
                self.TaskLock.release()
                task.perform()
                self.TaskLock.acquire()
                self.TaskQueue.open(tube_name)
                self.TaskLock.release()
                sleep(self.LoadInterval)
