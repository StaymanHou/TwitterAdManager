from TwitterMonitorTask import TwitterMonitorTask
import logging
import CampaignHelper
import re

class CreateTask(TwitterMonitorTask):
	"""docstring for CreateTask"""

	twitter_session = None
	camp = None

	def __init__(self, twitter_session, camp):
		super(CreateTask, self).__init__()
		self.twitter_session = twitter_session
		self.camp = camp

	def perform(self):
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


