import threading
import logging
import Config
from time import sleep
from MultiTubeQueue import MultiTubeQueue
import SessionHelper
import TaskHelper

class TwitterAdWorker(threading.Thread):
    """docstring for TwitterAdWorker"""
    
    config = None
    CheckInterval = 0
    TaskQueue = None
    TaskLock = None

    def __init__(self, TaskQueue, TaskLock):
        super(TwitterAdWorker, self).__init__()
        self.TaskQueue = TaskQueue
        self.TaskLock = TaskLock
        self.config = Config.get()
        self.CheckInterval = self.config.getint('Monitor_Worker', 'check_interval_in_sec')
        if self.CheckInterval < 1:
            raise Exception('TwitterAdWorker', 'check_interval_in_sec must be at least 1.')

    def run(self):
        logging.info('TwitterAdWorker started')
        while 1:
            sleep(self.CheckInterval)
            self.check()
        logging.info('TwitterAdWorker finished')

    def check(self):
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
                sleep(0)
