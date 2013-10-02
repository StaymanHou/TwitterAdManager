from TwitterMonitorTask import TwitterMonitorTask
import logging
import CampaignHelper
import re

class CreateTask(TwitterMonitorTask):
	"""This task will hold a reference of a :class:`Lib.TwitterSession.TwitterSession` 
		while initialized. Perform as a task to create a 'create_pending task' onto twitter server, 
		and update the localstatus to 'alive'(or 'create_fail' if failed).
	"""

	twitter_session = None
	camp = None

	def __init__(self, twitter_session, camp):
		super(CreateTask, self).__init__()
		self.twitter_session = twitter_session
		self.camp = camp

	def perform(self):
		"""Perform creating a 'create_pending task' onto twitter server, 
			and updating the localstatus to 'alive'(or 'create_fail' if failed).
			See abstract method :func:`Lib.TwitterMonitorTask.TwitterMonitorTask.perform`.
		"""
		url = self.twitter_session.get_root_url()+'/campaigns/create_promoted_account.json'
		payload = CampaignHelper.get_create_payload(self.camp, self.twitter_session)
		flag_success = True
		r = None
		try:
			r = self.twitter_session.post(url, data=payload, allow_redirects=False)
		except Exception, e:
			flag_success = False
		if flag_success and r.status_code==200 and re.search('campaignList:(.+?)"\}',r.text)!=None:
			new_id = long(re.search('campaignList:(.+?)"\}',r.text).group(1))
			CampaignHelper.set_campaign_created(self.camp, new_id=new_id)
			logging.info('@%s Create campaign [id=%d] succeeded.'%(self.twitter_session.account.username, self.camp.id))
		else:
			CampaignHelper.set_campaign_create_fail(self.camp)
			if not hasattr(r, 'status_code') or r.status_code is None:
				logging.warning('@%s Create campaign [pk=%d] failed. No response'%(self.twitter_session.account.username, self.camp.pk))
			else:
				logging.warning('@%s Create campaign [pk=%d] failed. Status code: %d'%(self.twitter_session.account.username, self.camp.pk, r.status_code))


