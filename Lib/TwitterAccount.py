from DB import DB

class TwitterAccount(object):
	"""docstring for TwitterAccount"""

	pk = 0
	fi_id = 0
	username = ''
	password = ''
	active = False
	budget_limit_threshold = 0.0
	acc_budget = 0.0
	acc_budget_remain = 0.0
	poor_zscore_threashold = 0.0
	effective_days = 7
	max_campaign_num = 200
	user_num_low = 0
	user_num_high = 0
	user_private_weight = 0.0
	intst_num_low = 0
	intst_num_high = 0
	intst_private_weight = 0.0
	cntry_num_low = 0
	cntry_num_high = 0
	cntry_private_weight = 0.0
	bid_low = 0.01
	bid_high = 0.01
	cmp_budget = 100.0
	daily_budget = 10.0
	pts = True
	gender = 0
	accelerated_delivery = True
	monitor_finished_hour = None
	controller_finished_hour = None
	update_time = None
	deleted = False

	def __init__(self):
		super(TwitterAccount, self).__init__()

	def get_list(active = True):
		db = DB()
		cur = db.execute(("SELECT *, DES_DECRYPT(`PSWD`,%s) AS DEPSWD FROM `Accounts` WHERE `ACTIVE`=%s", (db.key, int(active))))
		acc_list = []
		rows = cur.fetchall()
		for row in rows:
			acc = TwitterAccount()
			acc.pk = row['PK']
			acc.fi_id = row['FI_ID']
			acc.username = row['USERNAME']
			acc.password = row['DEPSWD']
			acc.active = row['ACTIVE']
			acc.budget_limit_threshold = row['BUDGET_LIMIT_THRESHOLD']
			acc.acc_budget = row['ACC_BUDGET']
			acc.acc_budget_remain = row['ACC_BUDGET_REMAIN']
			acc.poor_zscore_threshold = row['POOR_ZSCORE_THRESHOLD']
			acc.effective_days = row['EFFECTIVE_DAYS']
			acc.max_campaign_num = row['MAX_CAMPAIGN_NUM']
			acc.user_num_low = row['USER_NUM_LOW']
			acc.user_num_high = row['USER_NUM_HIGH']
			acc.user_private_weight = row['USER_PRIVATE_WEIGHT']
			acc.intst_num_low = row['INTST_NUM_LOW']
			acc.intst_num_high = row['INTST_NUM_HIGH']
			acc.intst_private_weight = row['INTST_PRIVATE_WEIGHT']
			acc.cntry_num_low = row['CNTRY_NUM_LOW']
			acc.cntry_num_high = row['CNTRY_NUM_HIGH']
			acc.cntry_private_weight = row['CNTRY_PRIVATE_WEIGHT']
			acc.bid_low = row['BID_LOW']
			acc.bid_high = row['BID_HIGH']
			acc.cmp_budget = row['CMP_BUDGET']
			acc.dly_budget = row['DLY_BUDGET']
			acc.pts = row['PTS']
			acc.gender = row['GENDER']
			acc.accelerated_delivery = row['ACCELERATED_DELIVERY']
			acc.monitor_finished_hour = row['MONITOR_FINISHED_HOUR']
			acc.controller_finished_hour = row['CONTROLLER_FINISHED_HOUR']
			acc.update_time = row['UPDATE_TIME']
			acc.deleted = row['DELETED']
			acc_list.append(acc)
		return acc_list

	get_list = staticmethod(get_list)