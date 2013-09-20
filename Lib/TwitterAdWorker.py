import threading
import logging

class TwitterAdWorker(threading.Thread):
    """docstring for TwitterAdWorker"""

    TaskQueue = None
    TaskLock = None

    def __init__(self, TaskQueue, TaskLock):
        super(TwitterAdWorker, self).__init__()
        self.TaskQueue = TaskQueue
        self.TaskLock = TaskLock

    def run(self):
        logging.info('TwitterAdWorker is running')
        

class TwitterFetcherThread (threading.Thread):
    def __init__(self, fetcherID, Fetcher_Config, Crawler_Work_Queue, Crawler_Work_Queue_Lock, Crawler_Data_Queue, Crawler_Data_Queue_Lock):
        threading.Thread.__init__(self)
        from MyDict import FETCHER_FLAGS_DICT
        self.FETCHER_FLAGS_DICT = FETCHER_FLAGS_DICT
        self.Fetcher_Config = Fetcher_Config
        self.fetcherID = fetcherID
        self.FETCHER_STATUS = 0
        self.FETCHER_FLAGS = self.FETCHER_FLAGS_DICT['Normal']
        self.Crawler_Work_Queue = Crawler_Work_Queue
        self.Crawler_Work_Queue_Lock = Crawler_Work_Queue_Lock
        self.Crawler_Data_Queue = Crawler_Data_Queue
        self.Crawler_Data_Queue_Lock = Crawler_Data_Queue_Lock

    def run(self):
        from time import sleep
        from TwitterParser import fetchaccinfo
        print "TwitterFetcher #%d start working!" % self.fetcherID
        # Get lock to synchronize threads
        while True:
            if not self.FETCHER_FLAGS & self.FETCHER_FLAGS_DICT['Normal']:
                self.FETCHER_STATUS = -1
                print "TwitterFetcher #%d something strange. exit!" % self.fetcherID
                sleep(0)
                return
            else:
                if self.FETCHER_FLAGS & self.FETCHER_FLAGS_DICT['Terminate']:
                    print "TwitterFetcher #%d stop by crawler. exit!" % self.fetcherID
                    self.FETCHER_STATUS = -2
                    sleep(0)
                    return
                else:
                    if self.FETCHER_FLAGS & self.FETCHER_FLAGS_DICT['Pause']:
                        self.FETCHER_STATUS = -3
                        sleep(self.Fetcher_Config['FETCHER_PAUSE_DURATION'])
                        continue
                    else:
                        self.FETCHER_STATUS = 1
                        self.Crawler_Work_Queue_Lock.acquire()
                        if self.Crawler_Work_Queue.empty():
                            self.Crawler_Work_Queue_Lock.release()
                            self.FETCHER_STATUS = -5
                            sleep(self.Fetcher_Config['FETCHER_PAUSE_DURATION'])
                            continue
                        else:
                            work_twt_username = self.Crawler_Work_Queue.get()
                            self.Crawler_Work_Queue_Lock.release()
                            #print 'fetching', work_twt_username#debug
                            temp_data = fetchaccinfo(work_twt_username)
                            temp_lst = [work_twt_username]
                            temp_lst.extend(temp_data)
                            while True:
                                self.Crawler_Data_Queue_Lock.acquire()
                                if self.Crawler_Data_Queue.full():
                                    self.Crawler_Data_Queue_Lock.release()
                                    self.FETCHER_STATUS = -7
                                    sleep(self.Fetcher_Config['FETCHER_DATAFULL_DURATION'])
                                    continue
                                else:
                                    #print 'put: '#debug
                                    self.Crawler_Data_Queue.put(temp_lst)
                                    self.Crawler_Data_Queue_Lock.release()
                                    self.FETCHER_STATUS = -8
                                    break
                            sleep(self.Fetcher_Config['FETCHER_FINISH_DURATION'])
                            continue

