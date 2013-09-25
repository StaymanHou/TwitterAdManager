from TwitterMonitorTask import TwitterMonitorTask
import logging
import CampaignHelper

class DeleteTask(TwitterMonitorTask):
	"""docstring for DeleteTask"""

	twitter_session = None
	camp = None

	def __init__(self, twitter_session, camp):
		super(DeleteTask, self).__init__()
		self.twitter_session = twitter_session
		self.camp = camp

	def perform(self):
		url = self.twitter_session.get_root_url()+'/campaigns/destroy'
		payload = CampaignHelper.get_delete_payload(self.camp, self.twitter_session)
		flay_success = True
		r = None
		try:
			r = self.twitter_session.post(url, data=payload, allow_redirects=False)
		except Exception, e:
			flay_success = False
		if flay_success and r.status_code==302:
			logging.info('@%s Delete campaign [id=%d] succeeded.'%(self.twitter_session.account.username, self.camp.id))
			CampaignHelper.set_campaign_deleted(self.camp)
		else:
			if r.status_code is None:
				logging.warning('@%s Delete campaign [id=%d] failed. No response'%(self.twitter_session.account.username, self.camp.id))
			else:
				logging.warning('@%s Delete campaign [id=%d] failed. Status code: %d'%(self.twitter_session.account.username, self.camp.id, r.status_code))
			CampaignHelper.set_campaign_delete_fail(self.camp)
