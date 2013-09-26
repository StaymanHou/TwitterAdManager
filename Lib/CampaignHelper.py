from LocalStatus import LocalStatus
from datetime import datetime
import Config
import pytz

def kill(camp):
	camp.local_status = LocalStatus.TitletoPK['Dead']
	camp.end_time = datetime.now()
	camp.active = False
	camp.save()

def update(campl, campo):
	pass

def create(campo):
	pass

def find_min_id(camp_list):
	if len(camp_list) == 0:
		return 0
	min_id = camp_list[0].id
	for camp in camp_list:
		if camp.id < min_id:
			min_id = camp.id
	return min_id

def get_delete_payload(camp, twitter_session):
	payload = {'utf8': u'\u2713',
			   'user': twitter_session.account.username,
			   'campaign_id': str(camp.id),
			   'authenticity_token': twitter_session.get_auth_token(),
			   '_method': 'delete'}
	return payload

def get_create_payload(camp, twitter_session):
	config = Config.get()
	local_tz = pytz.timezone(config.get('General', 'local_time_zone'))
	sf_tz = pytz.timezone('America/Los_Angeles')
	pts = 'off'
	if camp.pac_to_similar: pts = 'on'
	lt = 'any'
	if camp.locations.strip(): lt = 'specific'
	payload = {'utf8': u'\u2713',
			   'authenticity_token': twitter_session.get_auth_token(),
			   'campaign[name]': camp.name,
			   'campaign[io_id]': str(camp.fi_id),
			   'campaign_schedule': 'evergreen',#'custom' for custom start and end time
			   'campaign[start_date_only]': local_tz.localize(datetime.now()).astimezone(sf_tz).strftime('%Y-%m-%d'),
			   'campaign[end_date_only]': '',
			   'campaign[start_time_only]': local_tz.localize(datetime.now()).astimezone(sf_tz).strftime('%I:%M %p'),
			   'campaign[end_time_only]': '',
			   'primary_targeting_type': 'interest',
			   'is_promoted_account_campaign': 'true',
			   'campaign[keywords]': '  ',# why it's empty
			   'campaign[filter_negative_sentiment]': 'on',
			   'campaign[pac_to_similar]': pts,
			   'campaign[targeted_users]': camp.targeted_users,
			   'campaign[targeted_interests]': camp.targeted_interests,
			   'location_targeting': lt,# 'specific' for specific target
			   'campaign[locations]': camp.locations,# location code
			   'campaign[country_code]': '',# why it's empty
			   'campaign[gender]': str(camp.gender),
			   'campaign[total_budget_amount_local]': str(camp.total_budget),
			   'campaign[daily_budget_amount_local]': str(camp.daily_budget),
			   'campaign[accelerated_delivery]': str(bool(camp.accelerated_delivery)).lower(),
			   'campaign[bid_amount_local]': str(camp.max_bid)}
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

def set_campaign_created(camp, new_id):
	camp.id = new_id
	camp.local_status = LocalStatus.TitletoPK['Alive']
	camp.active = True
	camp.start_time = datetime.now()
	camp.save()

def set_campaign_create_fail(camp):
	camp.local_status = LocalStatus.TitletoPK['CreateFail']
	camp.active = False
	camp.start_time = datetime.now()
	camp.save()
