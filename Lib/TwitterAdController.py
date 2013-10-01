from multiprocessing import Process
from time import sleep
import logging
import Config
from TwitterAccount import TwitterAccount
import DateTimeHelper
import CampaignHelper
from datetime import datetime
from TwitterCampaign import TwitterCampaign

class TwitterAdController(object):
	"""This class operates as a controller. It controls the ads on the local 
		database. It does not perform any communication with twitter server. 
		It just checks if there are enough ads alive, generate new campaigns, 
		and delete poorly-performing ads.
	"""

	myprocess = None
	"""hold a :class:`multiprocessing.Process`."""

	def __init__(self):
		super(TwitterAdController, self).__init__()
		TACP = Process(target=self.OperateFunction, args=())
		self.myprocess = TACP

	def start(self):
		"""Start the process. Call :meth:`Lib.TwitterAdController.TwitterAdController.myprocess.start`."""
		self.myprocess.start()

	def join(self):
		"""Wait for the process to join. Call :meth:`Lib.TwitterAdController.TwitterAdController.myprocess.join`."""
		self.myprocess.join()

	def is_alive(self):
		"""Return a boolean indicates if myprocess is alive."""
		return self.myprocess.is_alive()

	def terminate(self):
		"""Terminate myprocess."""
		self.myprocess.terminate()

	def OperateFunction():
		"""This is a static method. Periodically, it checks all active accounts. 
			If the account meets the condition of commit a new check, it will do the following instructions.
			Get poorly-performing campaign list by calling :func:`Lib.CampaignHelper.get_poor_performance_camp_list`. 
			Put the poor campaigns into delete_pending by calling :func:`Lib.CampaignHelper.set_delete_pending`. 
			If number of alive campaigns is less than max_campaign_num, 
			generate create_pending campaigns to full by calling :func:`Lib.CampaignHelper.generate_createpending_camp`.
		"""
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
					PoorCmpList = CampaignHelper.get_poor_performance_camp_list(acc)
					dltnum = len(PoorCmpList)
					CampaignHelper.set_delete_pending(PoorCmpList)
					logging.info('@%s %d campaigns were pended to delete.'%(acc.username, dltnum))
				crtnum = acc.max_campaign_num - TwitterCampaign.get_alive_createpending_num(acc.fi_id)
				if crtnum > 0:
					CampaignHelper.generate_createpending_camp(acc, crtnum)
					logging.info('@%s %d campaigns were pended to create.'%(acc.username, crtnum))
				acc.set_controller_finished_hour(DateTimeHelper.floorbyday(datetime.now()))
			sleep(config.getint('Controller', 'check_interval_in_sec'));
		logging.info('Controller Process finished.')
	OperateFunction = staticmethod(OperateFunction)