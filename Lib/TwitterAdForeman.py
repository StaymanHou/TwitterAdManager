import threading
from time import sleep
import logging
import Config
import SessionHelper
import TaskHelper

class TwitterAdForeman(threading.Thread):
    """Foreman extends :class:`threading.Thread`. After starting, 
        it will periodically update sessions & account settings from database, 
        update :attr:`TaskQueue`, and update tasks.
    """

    config = None
    CheckInterval = 0
    TwitterSessions = []
    TaskQueue = None
    """It is responsible for the communication between :class:`Lib.TwitterAdForeman.TwitterAdForeman` 
        thread and :class:`Lib.TwitterAdWorker.TwitterAdWorker`  threads. It is an object of 
        :class:`Lib.MultiTubeQueue.MultiTubeQueue`.
    """
    TaskLock = None

    def __init__(self, TaskQueue, TaskLock):
        super(TwitterAdForeman, self).__init__()
        self.TaskQueue = TaskQueue
        self.TaskLock = TaskLock
        self.config = Config.get()
        self.CheckInterval = self.config.getint('Monitor_Foreman', 'check_interval_in_sec')
        if self.CheckInterval < 1:
            raise Exception('TwitterAdForeman', 'check_interval_in_sec must be at least 1.')

    def run(self):
        """Implement the interface of Thread. it Periodically calls 
            :meth:`Lib.TwitterAdForeman.TwitterAdForeman.check`.
        """
        logging.info('TwitterAdForeman thread started')
        while 1:
            self.check()
            sleep(self.CheckInterval)
        logging.info('TwitterAdForeman thread finished')

    def check(self):
        """Update :attr:TwitterSessions from local database by calling 
            :func:`Lib.SessionHelper.update_sessions`. 
            Update tasks and put into :attr:TaskQueue for 
            :class:`Lib.TwitterAdWorker.TwitterAdWorker` by calling 
            :func:`Lib.TaskHelper.update_taskqueue`.
        """
        self.TaskLock.acquire()
        SessionHelper.update_sessions(self.TwitterSessions, self.TaskQueue)
        TaskHelper.update_taskqueue(self.TaskQueue, self.TwitterSessions)
        self.TaskLock.release()
