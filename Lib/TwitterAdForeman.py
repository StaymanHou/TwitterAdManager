import threading
from time import sleep
import logging
import Config
import SessionHelper
import TaskHelper

class TwitterAdForeman(threading.Thread):
    """docstring for TwitterAdForeman"""

    config = None
    CheckInterval = 0
    TwitterSessions = []
    TaskQueue = None
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
        logging.info('TwitterAdForeman started')
        while 1:
            self.check()
            sleep(self.CheckInterval)
        logging.info('TwitterAdForeman finished')

    def check(self):
        self.TaskLock.acquire()
        SessionHelper.update_sessions(self.TwitterSessions, self.TaskQueue)
        TaskHelper.update_taskqueue(self.TaskQueue, self.TwitterSessions)
        self.TaskLock.release()
