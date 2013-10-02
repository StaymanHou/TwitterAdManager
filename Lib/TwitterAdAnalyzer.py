"""This is the helper for analyzing campaign performances of a given account.
"""

import json
from DB import DB
import DateTimeHelper
from numpy import mean,std
from datetime import datetime,timedelta
from TwitterCampaign import TwitterCampaign
from LocalStatus import LocalStatus

def GetIMPDistributionOneDay(fi_id,bid,time_limit=0,record_limit=10000):
    """This function calculates the distribution of the impressions versus one day. 

        :param fi_id: To specify the account.
        :param bid: The bid price should be given.
        :param time_limit: Only count the data within the time_limit. If 0, no limit.
        :param record_limit: Only this amount of campaigns will be take into account. 
        :returns: The average and standard deviation of the impressions of certain campaigns.
    """
    db = DB()
    query_tuple = ("SELECT START_TIME, DATA FROM Campaigns WHERE LOCAL_STATUS != 3 AND LOCAL_STATUS != 5 AND FI_ID = %s AND MAX_BID > %s AND MAX_BID < %s AND START_TIME > %s ORDER BY START_TIME DESC LIMIT %s",(fi_id,bid-0.005,bid+0.005,time_limit,record_limit))
    cur = db.execute(query_tuple)
    datalist = []
    for i in range(cur.rowcount):
        row = cur.fetchone()
        temp_start_time = row['START_TIME']
        temp_data = json.loads(row['DATA'])['impressions']
        startpartcut = temp_start_time.hour # if the first part of the data is not start from 0 o'clock than cut it to provide a whole day data
        temp_data = temp_data[startpartcut:]
        if len(temp_data)<24:
            continue
        datalist.append(sum(temp_data[:24]))
    distribution = {'ave':-1,'std':1}
    if len(datalist)!=0:
        distribution['ave'] = mean(datalist)
        distribution['std'] = std(datalist)
    return distribution

def GetPoorPfmcCmpListIMPBased(account):
    """Get the poor performance campaign list based on imporession.
        It calls :func:`Lib.TwitterAdAnalyzer.GetIMPDistributionOneDay` for distribution of the data.

        :param account: To specify the account.
        :returns: A list of :class:`Lib.TwitterCampaign.TwitterCampaign` whose performance are poor based on static analysis.
    """
    # if u change the account setting, the distribution will be based on the campaigns generated after the changing
    alive_cmp_lst = TwitterCampaign.get_list(account.fi_id, local_status=LocalStatus.TitletoPK['Alive'])
    dist_dict = {}
    dltpd_cmp_lst = []
    for alv_cmp in alive_cmp_lst:
        startpartcut = alv_cmp.start_time.hour
        temp_data = alv_cmp.data['impressions'][startpartcut:]
        if len(temp_data)<24:
            continue
        if alv_cmp.max_bid not in dist_dict:
            time_limit = datetime.now()-timedelta(days=account.effective_days)
            if account.update_time>time_limit: time_limit = account.update_time
            dist_dict[alv_cmp.max_bid] = GetIMPDistributionOneDay(account.fi_id,alv_cmp.max_bid,time_limit=time_limit)
        zscore = (sum(temp_data[-24:]) - dist_dict[alv_cmp.max_bid]['ave'])/dist_dict[alv_cmp.max_bid]['std']
        if zscore<(account.poor_zscore_threshold):
            dltpd_cmp_lst.append(alv_cmp)
    return dltpd_cmp_lst
