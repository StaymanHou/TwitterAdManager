"""This is the helper for :class:`Lib.TwitterCampaign.TwitterCampaign`. 
	Dealing with the operations related to TwitterCampaign.
"""

from LocalStatus import LocalStatus
from datetime import datetime
import Config
import pytz
import TwitterAdAnalyzer
import TwitterAdGenerator
from TwitterCampaign import TwitterCampaign
from MyFunction import Username2Userid

def get_poor_performance_camp_list(account):
	"""Return a list of all alive TwitterCampaigns of the account if 
		poor_zscore_threshold <= -99.
		Otherwise, return the result of :func:`Lib.TwitterAdAnalyzer.TwitterAdAnalyzer.GetPoorPfmcCmpListIMPBased` call.
	"""
	if account.poor_zscore_threshold <= -99:
		return TwitterCampaign.get_list(account.fi_id, local_status=LocalStatus.TitletoPK['Alive'])
	return TwitterAdAnalyzer.GetPoorPfmcCmpListENGBased(account)

def set_delete_pending(camp_list):
	"""Set the campaigns in the camp_list into 'deletepending'.
	"""
	for camp in camp_list:
		camp.local_status = LocalStatus.TitletoPK['DeletePending']
		camp.save()

def generate_createpending_camp(account, generate_num):
	"""Generate certain number of new campaigns and put into 'createpending'.
		Calls :func:`Lib.TwitterAdGenerator.TwitterAdGenerator.crtpd2refillcmp`.
	"""
	TwitterAdGenerator.crtpd2refillcmp(account, generate_num)

def kill(camp):
	"""Kill the given campaign. Set it into dead, active = False, and end_time = now.
	"""
	camp.local_status = LocalStatus.TitletoPK['Dead']
	camp.end_time = datetime.now()
	camp.active = False
	camp.save()

def update(campl, campo):
	"""Update the data of an local campaign with an online campaign object.
		\n..note::
		\n\tThe online campaign object is slitely diff. It's data attribute 
		only holds the value of a certain hour. Not a list.

		>>> campo.data = {'spend': 1.23,
		>>> 			  'impressions': 1000,
		>>>				  'engagements': 123}

	"""
	campl.data['spend'].append(campo.data['spend'])
	campl.data['total_spend'] += campo.data['spend']
	campl.data['impressions'].append(campo.data['impressions'])
	campl.data['total_impressions'] += campo.data['impressions']
	campl.data['engagements'].append(campo.data['engagements'])
	campl.data['total_engagements'] += campo.data['engagements']
	campl.save()

def create(campo):
	"""Create a new campaign with an online campaign object.
		\n..note::
		\n\tThe online campaign object is slitely diff. It's data attribute 
		only holds the value of a certain hour. Not a list.

		>>> campo.data = {'spend': 1.23,
		>>> 			  'impressions': 1000,
		>>>				  'engagements': 123}

	"""
	campo.data['total_spend'] = campo.data['spend']
	campo.data['spend'] = [campo.data['spend']]
	campo.data['total_impressions'] = campo.data['impressions']
	campo.data['impressions'] = [campo.data['impressions']]
	campo.data['total_engagements'] = campo.data['engagements']
	campo.data['engagements'] = [campo.data['engagements']]
	campo.save()

def find_min_id(camp_list):
	"""Return the min id among all ids of alive campaigns in this camp_list.
		Return 0 if there's no camp in the list
	"""
	if len(camp_list) == 0:
		return 0
	min_id = camp_list[0].id
	for camp in camp_list:
		if camp.id < min_id:
			min_id = camp.id
	return min_id

def get_delete_payload(camp, twitter_session):
	"""Return a delete payload out of a campaign and a twitter_session 
		for a twitter delete request.
	"""
	payload = {'utf8': u'\u2713',
			   'user': twitter_session.account.username,
			   'campaign_id': str(camp.id),
			   'authenticity_token': twitter_session.get_auth_token(),
			   '_method': 'delete'}
	return payload

def get_create_payload(camp, twitter_session):
	"""Return a create payload out of a campaign and a twitter_session 
		for a twitter create request.
	"""
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
			   'tv_targeting_type': 'tv_shows',
			   'campaign[targeted_tv_shows]': '',
			   'location_targeting': lt,# 'specific' for specific target
			   'campaign[locations]': camp.locations,# location code
			   'campaign[country_code]': '',# why it's empty
			   'campaign[gender]': str(camp.gender),
			   'rendered_without_broad_match_targeting': 'false',
			   'cursor': '',
			   'open_timeline': 'true',
			   'new_tweets': '',
			   'new_scheduled_tweets': '',
			   'campaign[total_budget_amount_local]': str(camp.total_budget),
			   'campaign[daily_budget_amount_local]': str(camp.daily_budget),
			   'campaign[accelerated_delivery]': str(bool(camp.accelerated_delivery)).lower(),
			   'campaign[bid_amount_local]': str(camp.max_bid)}
	return payload

def set_campaign_deleted(camp):
	"""Set a camp into dead
	"""
	camp.local_status = LocalStatus.TitletoPK['Dead']
	camp.active = False
	camp.end_time = datetime.now()
	camp.save()

def set_campaign_delete_fail(camp):
	"""Set a camp into deletefail
	"""
	camp.id = 0
	camp.local_status = LocalStatus.TitletoPK['DeleteFail']
	camp.active = False
	camp.end_time = datetime.now()
	camp.save()

def set_campaign_created(camp, new_id):
	"""Set a camp into alive
	"""
	camp.id = new_id
	camp.local_status = LocalStatus.TitletoPK['Alive']
	camp.active = True
	camp.start_time = datetime.now()
	camp.save()

def set_campaign_create_fail(camp):
	"""Set a camp into createfail
	"""
	camp.local_status = LocalStatus.TitletoPK['CreateFail']
	camp.active = False
	camp.start_time = datetime.now()
	camp.save()
