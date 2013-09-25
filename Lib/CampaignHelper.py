from LocalStatus import LocalStatus
from datetime import datetime

def get_delete_payload(camp, twitter_session):
	payload = {'utf8': u'\u2713',
			   'user': twitter_session.account.username,
			   'campaign_id': str(camp.id),
			   'authenticity_token': twitter_session.get_auth_token(),
			   '_method': 'delete'}
	return payload

def set_campaign_deleted(camp):
	camp.local_status = LocalStatus.TitletoPK['Dead']
	camp.active = False
	camp.end_time = datetime.now()
	camp.save()

def set_campaign_delete_fail(camp):
	camp.id = 0
	camp.local_status = LocalStatus.TitletoPK['DeleteFail']
	camp.active = False
	camp.end_time = datetime.now()
	camp.save()
