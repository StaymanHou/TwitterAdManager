import threading
import time

import threading
import logging

class TwitterAdForeman(threading.Thread):
    """docstring for TwitterAdForeman"""

    Sessions = None
    TaskLists = None
    TaskQueue = None
    TaskLock = None

    def __init__(self, TaskQueue, TaskLock):
        super(TwitterAdForeman, self).__init__()
        self.TaskQueue = TaskQueue
        self.TaskLock = TaskLock

    def run(self):
        logging.info('TwitterAdForeman is running')

def IntSecNow():
  return int(time.mktime(time.localtime()))

class TwitterForemanThread (threading.Thread):
    def __init__(self, foremanID, Foreman_Config, Crawler_Work_Queue, Crawler_Work_Queue_Size, Crawler_Work_Queue_Lock, Crawler_Data_Queue, Crawler_Data_Queue_Size, Crawler_Data_Queue_Lock, Work_DB_Path, Data_DB_Path, Init_Work=None):
        threading.Thread.__init__(self)
        from MyDict import FOREMAN_FLAGS_DICT
        self.FOREMAN_FLAGS_DICT = FOREMAN_FLAGS_DICT
        self.Foreman_Config = Foreman_Config
        self.foremanID = foremanID
        self.FOREMAN_STATUS = 0
        self.FOREMAN_FLAGS = self.FOREMAN_FLAGS_DICT['Normal']
        self.Crawler_Work_Queue = Crawler_Work_Queue
        self.Crawler_Work_Queue_Size = Crawler_Work_Queue_Size
        self.Crawler_Work_Queue_Lock = Crawler_Work_Queue_Lock
        self.Crawler_Data_Queue = Crawler_Data_Queue
        self.Crawler_Data_Queue_Size = Crawler_Data_Queue_Size
        self.Crawler_Data_Queue_Lock = Crawler_Data_Queue_Lock
        self.Work_DB_Path = Work_DB_Path
        self.Data_DB_Path = Data_DB_Path
        self.Init_Work = Init_Work
        self.timestamp = IntSecNow()
        self.speed = None
        self.total_status = 0
        self.total_data_num = 0

    def run(self):
        from time import sleep
        from TwitterDB import dataliststore, TwitterWorkDB
        print "TwitterForeman #%d start working!" % self.foremanID
        WorkDB = TwitterWorkDB.open(self.Work_DB_Path)
        if not WorkDB.empty(): self.total_data_num = long(WorkDB.DB[WorkDB.finishpointer]) # added in May 6 2013: don't want to the total num back to 0 after resume
        if self.Init_Work!=None:
            for work in self.Init_Work:
                WorkDB.put(work)
        # Get lock to synchronize threads
        while True:
            if not self.FOREMAN_FLAGS & self.FOREMAN_FLAGS_DICT['Normal']:
                self.FOREMAN_STATUS = -1
                WorkDB.close()
                print "TwitterForeman #%d something strange. exit!" % self.foremanID
                sleep(0)
                return
            else:
                if self.FOREMAN_FLAGS & self.FOREMAN_FLAGS_DICT['Terminate']:
                    self.FOREMAN_STATUS = -2
                    WorkDB.close()
                    print "TwitterForeman #%d stop by crawler. exit!" % self.foremanID
                    sleep(0)
                    return
                else:
                    if self.FOREMAN_FLAGS & self.FOREMAN_FLAGS_DICT['Pause']:
                        self.FOREMAN_STATUS = -3
                        sleep(self.Foreman_Config['FOREMAN_PAUSE_DURATION'])
                        continue
                    else:
                        self.FOREMAN_STATUS = 1
                        self.Crawler_Work_Queue_Lock.acquire()
                        self.Crawler_Data_Queue_Lock.acquire()
                        if not (self.Crawler_Work_Queue.empty() or float(self.Crawler_Work_Queue.qsize())/self.Crawler_Work_Queue_Size<0.1 or self.Crawler_Data_Queue.full() or float(self.Crawler_Data_Queue.qsize())/self.Crawler_Data_Queue_Size>0.9):
                            self.Crawler_Data_Queue_Lock.release()
                            self.Crawler_Work_Queue_Lock.release()
                            self.FOREMAN_STATUS = -4
                            sleep(self.Foreman_Config['FOREMAN_NOWORK_DURATION'])
                            continue
                        else:
                            self.Crawler_Work_Queue_Lock.release()
                            temp_data_list = []
                            while not self.Crawler_Data_Queue.empty():
                                temp_data_list.append(self.Crawler_Data_Queue.get())
                            self.Crawler_Data_Queue_Lock.release()
                            now = IntSecNow()
                            if self.speed == None:
                                self.speed = 0
                            else:
                                newspeed = float(len(temp_data_list))/(now-self.timestamp)
                                self.speed = self.speed/2 + newspeed/2
                            self.timestamp = now
                            self.total_data_num += len(temp_data_list)
                            print '\n---[Fetching speed: %.3f acc/s | Totally %s acc fetched]---\n'%(self.speed,"{:,}".format(self.total_data_num))
                            if len(temp_data_list)>0:
                                self.total_status = 0
                            dataliststore(temp_data_list, WorkDB, self.Data_DB_Path)
                            if WorkDB.empty():
                                self.total_status -= 1#finished suspiciously
                            self.Crawler_Work_Queue_Lock.acquire()
                            while not self.Crawler_Work_Queue.full():
                                if WorkDB.empty():
                                    break
                                else:
                                    self.Crawler_Work_Queue.put(WorkDB.get())
                            self.Crawler_Work_Queue_Lock.release()
                            self.FOREMAN_STATUS = -5
                            sleep(self.Foreman_Config['FOREMAN_FINISH_DURATION'])
                            continue

