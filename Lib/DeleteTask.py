from TwitterMonitorTask import TwitterMonitorTask
import logging
import CampaignHelper

class DeleteTask(TwitterMonitorTask):
	"""This task will hold a reference of a :class:`Lib.TwitterSession.TwitterSession` 
		while initialized. Perform as a task to delete a 'delete_pending task' on twitter server, 
		and update the localstatus to 'dead'(or 'delete_fail' if failed).
	"""
	twitter_session = None
	camp = None

	def __init__(self, twitter_session, camp):
		super(DeleteTask, self).__init__()
		self.twitter_session = twitter_session
		self.camp = camp

	def perform(self):
		"""Perform deleting a 'delete_pending task' on twitter server, 
			and updating the localstatus to 'dead'(or 'delete_fail' if failed).
			See abstract method :func:`Lib.TwitterMonitorTask.TwitterMonitorTask.perform`.
		"""
		url = self.twitter_session.get_root_url()+'/campaigns/destroy'
		payload = CampaignHelper.get_delete_payload(self.camp, self.twitter_session)
		flag_success = True
		r = None
		try:
			r = self.twitter_session.post(url, data=payload, allow_redirects=False)
		except Exception, e:
			flag_success = False
		if flag_success and r.status_code==302:
			CampaignHelper.set_campaign_deleted(self.camp)
			logging.info('@%s Delete campaign [id=%d] succeeded.'%(self.twitter_session.account.username, self.camp.id))
		else:
			CampaignHelper.set_campaign_delete_fail(self.camp)
			if r.status_code is None:
				logging.warning('@%s Delete campaign [id=%d] failed. No response'%(self.twitter_session.account.username, self.camp.id))
			else:
				logging.warning('@%s Delete campaign [id=%d] failed. Status code: %d'%(self.twitter_session.account.username, self.camp.id, r.status_code))
