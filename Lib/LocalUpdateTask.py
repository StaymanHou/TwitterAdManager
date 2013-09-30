from TwitterMonitorTask import TwitterMonitorTask
import logging
import re
from TwitterCampaign import TwitterCampaign
from LocalStatus import LocalStatus
import json
import Config
import CampaignHelper
from LocalStatus import LocalStatus
from datetime import datetime, timedelta
import time
from time import sleep
import DateTimeHelper
from TwitterSummary import TwitterSummary

class LocalUpdateTask(TwitterMonitorTask):
	"""docstring for LocalUpdateTask"""

	twitter_session = None
	hour_start = None
	camp_local_list = []
	camp_online_list = []

	def __init__(self, twitter_session, hour_start):
		super(LocalUpdateTask, self).__init__()
		self.twitter_session = twitter_session
		self.hour_start = hour_start

	def perform(self):
		"""invoke self.do() until success: return 0"""
		
		while self.do():
			logging.info('@%s Local Update for %s failed. Retry'%(self.twitter_session.account.username, self.hour_start.__str__()))
		logging.info('@%s Local Update for %s succeeded.'%(self.twitter_session.account.username, self.hour_start.__str__()))

	def do(self):
		"""return negative if fail, return 0 if succeed"""
		status = self.get_local_list()
		if status != 0:
			return status
		status = self.get_online_list()
		if status != 0:
			return status
		status = self.update_summary()
		if status != 0:
			return status
		status = self.remove_camp_local_no_online()
		if status != 0:
			return status
		status = self.update_exist()
		if status != 0:
			return status
		status = self.create_new()
		if status != 0:
			return status
		return 0

	def get_local_list(self):
		self.camp_local_list = TwitterCampaign.get_list(self.twitter_session.account.fi_id, local_status=LocalStatus.TitletoPK['Alive'])
		return 0

	def get_online_list(self):
		"""not only this hour's list but also this hour's data"""
		config = Config.get()
		cursor = ''
		for i in range(config.getint('Monitor', 'max_campaign_scan_pages')):
			url = self.twitter_session.get_root_url()+'/campaigns_dashboard/data'
			payload = {'user': self.twitter_session.account.username,
					   'cursor': cursor,
					   'granularity': 'hour',
					   'start': str(int(time.mktime(self.hour_start.timetuple()))),
					   'end': str(int(time.mktime((self.hour_start+DateTimeHelper.onehour).timetuple()))),
					   'clients': 'false',
					   'category': 'tc:t',
					   'fi': str(self.twitter_session.account.fi_id),
					   'campaign_list': ''}
			try:
				r = self.twitter_session.get(url, params=payload)
			except Exception, e:
				logging.warning('@%s No response while loading %s'%(self.twitter_session.account.username, url))
				return -1
			if r.status_code!=200:
				logging.warning('@%s Unexpected response while loading %s | Status code: %d'%(self.twitter_session.account.username, url, r.status_code))
				return -2
			campaign_data = json.loads(r.text)
			self.camp_online_list = []
			# fetch data
			for key, value in campaign_data['campaigns'].iteritems():
				if value['active']:
					camp = TwitterCampaign()
					camp.id = int(key)
					camp.name = value['name']
					camp.local_status = LocalStatus.TitletoPK['Alive']
					camp.active = True
					camp.start_time = datetime.fromtimestamp(value['start_time']/1000)
					camp.fi_id = value['fi_id']
					camp.total_budget = value['total_budget']
					camp.daily_budget = value['daily_budget']
					camp.max_bid = float(value['max_bid'])
					data = value['data']
					camp.data['spend'] = 0
					if 'spend_from_db' in data and len(data['spend_from_db'])>0 and data['spend_from_db'][-1]>0:
						camp.data['spend'] = data['spend_from_db'][-1]
					camp.data['engagements'] = 0
					if 'engagements' in data and 'follows' in data['engagements'] and 'values' in data['engagements']['follows'] and len(data['engagements']['follows']['values'])>0 and data['engagements']['follows']['values'][-1]>0:
						camp.data['engagements'] = data['engagements']['follows']['values'][-1]
					camp.data['impressions'] = 0
					if 'impressions' in data and 'values' in data['impressions'] and len(data['impressions']['values'])>0 and data['impressions']['values'][-1]>0:
						camp.data['impressions'] = data['impressions']['values'][-1]
					camp.pac_to_similar = value['is_pac']
					self.camp_online_list.append(camp)
			# set cursor
			new_cursor = campaign_data['cursor']['next']
			if new_cursor=='':
				break
			if int(re.search(':(.+?)$', new_cursor).group(1)) <= CampaignHelper.find_min_id(self.camp_local_list):
				break
			cursor = new_cursor
		return 0

	def update_summary(self):
		summary = TwitterSummary.get_last(self.twitter_session.account.fi_id)
		summary.new_spend = 0
		summary.new_engagements = 0
		summary.new_impressions = 0
		for camp in self.camp_online_list:
			summary.new_spend += camp.data['spend']
			summary.new_engagements += camp.data['engagements']
			summary.new_impressions += camp.data['impressions']
		summary.total_spend += summary.new_spend
		summary.total_engagements += summary.new_engagements
		summary.total_impressions += summary.new_impressions
		summary.period_start = self.hour_start
		summary.period_end = self.hour_start+DateTimeHelper.onehour
		summary.save()
		return 0

	def remove_camp_local_no_online(self):
		"""self.camp_local_list should be modified so that there is no dead"""
		online_id_list = [camp.id for camp in self.camp_online_list]
		for camp in list(self.camp_local_list):
			if camp.id not in online_id_list:
				CampaignHelper.kill(camp)
				self.camp_local_list.remove(camp)
		return 0

	def update_exist(self):
		"""self.camp_online_list should be modified so that there is no exist"""
		camp_local_dict = {}
		for camp in self.camp_local_list:
			camp_local_dict[camp.id] = camp
		for campo in list(self.camp_online_list):
			if campo.id in camp_local_dict:
				campl = camp_local_dict[campo.id]
				CampaignHelper.update(campl, campo)
				self.camp_online_list.remove(campo)
		return 0

	def create_new(self):
		for camp in self.camp_online_list:
			CampaignHelper.create(camp)
		return 0
