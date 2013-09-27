from multiprocessing import Process
from time import sleep
import logging
import Config
from TwitterAccount import TwitterAccount
import DateTimeHelper
import CampaignHelper

class TwitterAdController(object):
	"""docstring for TwitterAdController"""

	myprocess = None

	def __init__(self):
		super(TwitterAdController, self).__init__()
		TACP = Process(target=self.OperateFunction, args=())
		self.myprocess = TACP

	def start(self):
		self.myprocess.start()

	def join(self):
		self.myprocess.join()

	def OperateFunction():
		config = Config.get()
		logging.info('Controller Process started.')
		while 1:
			acc_list = TwitterAccount.get_list()
			for acc in acc_list:
				if acc.monitor_finished_hour is None:
					continue
				if acc.controller_finished_hour is None:
					acc.controller_finished_hour = DateTimeHelper.floorbyday(datetime.now())-DateTimeHelper.oneday
				if datetime.now() >= acc.controller_finished_hour+DateTimeHelper.oneday and acc.monitor_finished_hour+DateTimeHelper.oneday >= acc.monitor_finished_hour:
					PoorCmpList = CampaignHelper.get_poor_performance_camp_list(acc.fi_id)
					dltnum = len(PoorCmpList)
					CampaignHelper.set_delete_pending(PoorCmpList)
					logging.info('@%s %d campaigns were pended to delete.'%(acc.username, dltnum))
				crtnum = acc.max_campaign_num - TwitterCampaign.get_alive_createpending_num(acc.fi_id)
				if crtnum > 0:
					CampaignHelper.generate_createpending_camp(acc.fi_id)
					logging.info('@%s %d campaigns were pended to create.'%(acc.username, crtnum))
				acc.set_controller_finished_hour(DateTimeHelper.floorbyday(datetime.now()))

				acc['CONTROLLER_FINISHED_HOUR'] = floorbyday(datetime.now())
				MydbSetAccControllerFinishedHour(acc['FI_ID'], acc['CONTROLLER_FINISHED_HOUR'])
			sleep(config.getint('Controller', 'check_interval_in_sec'));
		logging.info('Controller Process finished.')
	OperateFunction = staticmethod(OperateFunction)