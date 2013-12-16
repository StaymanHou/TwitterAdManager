"""This is the helper for analyzing campaign performances of a given account.
"""

import json
from DB import DB
from numpy import mean,std
from datetime import datetime,timedelta
from TwitterCampaign import TwitterCampaign
from LocalStatus import LocalStatus
from MyFunction import Userid2Username, Intstid2Intstname

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

def GetENGDistributionOneDay(fi_id,bid,time_limit=0,record_limit=10000):
    """This function calculates the distribution of the engagements versus one day. 

        :param fi_id: To specify the account.
        :param bid: The bid price should be given.
        :param time_limit: Only count the data within the time_limit. If 0, no limit.
        :param record_limit: Only this amount of campaigns will be take into account. 
        :returns: The average and standard deviation of the engagements of certain campaigns.
    """
    db = DB()
    query_tuple = ("SELECT START_TIME, DATA FROM Campaigns WHERE LOCAL_STATUS != 3 AND LOCAL_STATUS != 5 AND FI_ID = %s AND MAX_BID > %s AND MAX_BID < %s AND START_TIME > %s ORDER BY START_TIME DESC LIMIT %s",(fi_id,bid-0.005,bid+0.005,time_limit,record_limit))
    cur = db.execute(query_tuple)
    datalist = []
    for i in range(cur.rowcount):
        row = cur.fetchone()
        temp_start_time = row['START_TIME']
        temp_data = json.loads(row['DATA'])['engagements']
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

def GetPoorPfmcCmpListENGBased(account):
    """Get the poor performance campaign list based on engagement.
        It calls :func:`Lib.TwitterAdAnalyzer.GetENGDistributionOneDay` for distribution of the data.

        :param account: To specify the account.
        :returns: A list of :class:`Lib.TwitterCampaign.TwitterCampaign` whose performance are poor based on static analysis.
    """
    # if u change the account setting, the distribution will be based on the campaigns generated after the changing
    alive_cmp_lst = TwitterCampaign.get_list(account.fi_id, local_status=LocalStatus.TitletoPK['Alive'])
    dist_dict = {}
    dltpd_cmp_lst = []
    for alv_cmp in alive_cmp_lst:
        startpartcut = alv_cmp.start_time.hour
        temp_data = alv_cmp.data['engagements'][startpartcut:]
        if len(temp_data)<24:
            continue
        if alv_cmp.max_bid not in dist_dict:
            time_limit = datetime.now()-timedelta(days=account.effective_days)
            if account.update_time>time_limit: time_limit = account.update_time
            dist_dict[alv_cmp.max_bid] = GetENGDistributionOneDay(account.fi_id,alv_cmp.max_bid,time_limit=time_limit)
        zscore = (sum(temp_data[-24:]) - dist_dict[alv_cmp.max_bid]['ave'])/dist_dict[alv_cmp.max_bid]['std']
        if zscore<(account.poor_zscore_threshold):
            dltpd_cmp_lst.append(alv_cmp)
    return dltpd_cmp_lst

#----------------------------------------------------------------------------------------------------------------#
################################################# only for testing ###############################################
#----------------------------------------------------------------------------------------------------------------#

def WriteIMPDistributionOneDay(fi_id,bid,time_limit=0,record_limit=10000):
    cur = MydbExec(("SELECT ID, START_TIME, DATA FROM Campaigns WHERE LOCAL_STATUS != 3 AND LOCAL_STATUS != 5 AND FI_ID = %s AND MAX_BID > %s AND MAX_BID < %s AND START_TIME > %s ORDER BY START_TIME DESC LIMIT %s",(fi_id,bid-0.005,bid+0.005,time_limit,record_limit)))
    datalist = []
    fp = open('testref.txt','a')
    for i in range(cur.rowcount):
        row = cur.fetchone()
        temp_start_time = row['START_TIME']
        temp_data = json.loads(row['DATA'])['impressions']
        startpartcut = temp_start_time.hour # if the first part of the data is not start from 0 o'clock than cut it to provide a whole day data
        temp_data = temp_data[startpartcut:]
        if len(temp_data)<24:
            continue
        datalist.append(sum(temp_data[:24]))
        fp.write(str(row['ID'])+'\t'+str(temp_data)+'\t'+str(sum(temp_data[:24]))+'\n')
    distribution = {'ave':-1,'std':1}
    if len(datalist)!=0:
        distribution['ave'] = mean(datalist)
        distribution['std'] = std(datalist)
    fp.write('dist\t'+str(distribution['ave'])+'\t'+str(distribution['std']))
    fp.close()
    return

def WritePoorPfmcCmpListIMPBased(fi_id):
    conf = MydbGetAccConfForAnlz(fi_id)
    # if u change the account setting, the distribution will be based on the campaigns generated after the changing
    alive_cmp_lst = MydbGetAliveCmpList(fi_id)
    fp = open('testalv.txt','a')
    dist_dict = {}
    dltpd_cmpid_lst = []
    for alv_cmp in alive_cmp_lst:
        startpartcut = alv_cmp['start_time'].hour
        temp_data = json.loads(alv_cmp['data'])['impressions'][startpartcut:]
        if len(temp_data)<24:
            continue
        if alv_cmp['bid'] not in dist_dict:
            dist_dict[alv_cmp['bid']] = GetIMPDistributionOneDay(fi_id,alv_cmp['bid'],time_limit=conf['UPDATE_TIME'])
        zscore = (sum(temp_data[-24:]) - dist_dict[alv_cmp['bid']]['ave'])/dist_dict[alv_cmp['bid']]['std']
        fp.write(str(alv_cmp['id'])+'\t'+str(temp_data)+'\t'+str(sum(temp_data[-24:]))+'\t'+str(zscore)+'\n')
        if zscore<(conf['POOR_ZSCORE_THRESHOLD']):
            dltpd_cmpid_lst.append(alv_cmp['id'])
    fp.write('dltlist\t'+str(dltpd_cmpid_lst))
    fp.close()
    return

def WriteIMPPHVerseUserAndNum():
    db = DB()
    query_tuple = ("SELECT TARGETED_USERS, DATA FROM Campaigns WHERE 1",())
    cur = db.execute(query_tuple)

    fp3 = open('testuserid.txt','w')
    fp4 = open('testusernum.txt','w')
    userid_dict = {}
    usernum_dict = {}
    print 'record num: %d'%cur.rowcount
    for i in range(cur.rowcount):
        row = cur.fetchone()
        temp_user = row['TARGETED_USERS']
        if temp_user==None: continue
        if len(temp_user)==0: continue
        temp_user = temp_user.split(',')
        temp_data = json.loads(row['DATA'])['impressions']
        if temp_data == []: continue
        if len(temp_user) not in usernum_dict:
            usernum_dict[len(temp_user)] = []
        usernum_dict[len(temp_user)].extend(temp_data)
        for user in temp_user:
            if user not in userid_dict:
                userid_dict[user] = []
            userid_dict[user].extend(temp_data)

    fp3.write('total\t'+str(len(userid_dict))+'\n')
    for userid in userid_dict:
        fp3.write(userid+'\t'+str(len(userid_dict[userid]))+'\t'+str(mean(userid_dict[userid]))+'\t'+str(std(userid_dict[userid]))+'\n')
    fp3.close()

    fp4.write('total\t'+str(len(usernum_dict))+'\n')
    for usernum in usernum_dict:
        fp4.write(str(usernum)+'\t'+str(len(usernum_dict[usernum]))+'\t'+str(mean(usernum_dict[usernum]))+'\t'+str(std(usernum_dict[usernum]))+'\n')
    fp4.close()

def WriteENGPHVerseUser(FI_ID):
    db = DB()
    query_tuple = ("SELECT TARGETED_USERS, DATA FROM Campaigns WHERE FI_ID = %s",(FI_ID,))
    cur = db.execute(query_tuple)

    fp3 = open('Analyze_result_user.txt','w')
    userid_dict = {}
    print 'record num: %d'%cur.rowcount
    for i in range(cur.rowcount):
        row = cur.fetchone()
        temp_user = row['TARGETED_USERS']
        if temp_user==None: continue
        if len(temp_user)==0: continue
        temp_user = temp_user.split(',')
        temp_data = json.loads(row['DATA'])['engagements']
        if temp_data == []: continue
        for user in temp_user:
            if user not in userid_dict:
                userid_dict[user] = []
            userid_dict[user].extend(temp_data)

    fp3.write('total\t'+str(len(userid_dict))+'\n')
    fp3.write('userid\thours\tave\tstd\tusername\n')
    for userid in userid_dict:
        fp3.write(str(userid)+'\t'+str(len(userid_dict[userid]))+'\t'+str(mean(userid_dict[userid]))+'\t'+str(std(userid_dict[userid]))+'\t'+Userid2Username(userid)+'\n')
    fp3.close()

def WriteENGPHVerseIntst(FI_ID):
    db = DB()
    query_tuple = ("SELECT TARGETED_INTERESTS, DATA FROM Campaigns WHERE FI_ID = %s",(FI_ID,))
    cur = db.execute(query_tuple)

    fp3 = open('Analyze_result_intrest.txt','w')
    intstid_dict = {}
    print 'record num: %d'%cur.rowcount
    for i in range(cur.rowcount):
        row = cur.fetchone()
        temp_interest = row['TARGETED_INTERESTS']
        if temp_interest==None: continue
        if len(temp_interest)==0: continue
        temp_interest = temp_interest.split(',')
        temp_data = json.loads(row['DATA'])['engagements']
        if temp_data == []: continue
        for interest in temp_interest:
            if interest not in intstid_dict:
                intstid_dict[interest] = []
            intstid_dict[interest].extend(temp_data)

    fp3.write('total\t'+str(len(intstid_dict))+'\n')
    fp3.write('interestid\thours\tave\tstd\tinterest\n')
    for intstid in intstid_dict:
        fp3.write(str(intstid)+'\t'+str(len(intstid_dict[intstid]))+'\t'+str(mean(intstid_dict[intstid]))+'\t'+str(std(intstid_dict[intstid]))+'\t'+Intstid2Intstname(intstid)+'\n')
    fp3.close()

def WriteIMPPHVerseBid(PK=1900, FI_ID=30269805):
    cur = MydbExec(("SELECT MAX_BID, DATA FROM Campaigns WHERE PK>%s AND FI_ID=%s",(PK, FI_ID)))
    fp = open('impvsdib.txt','a')
    bid_dict = {}
    print 'record num: %d'%cur.rowcount
    for i in range(cur.rowcount):
        row = cur.fetchone()
        temp_bid = row['MAX_BID']
        if temp_bid==None: continue
        temp_data = json.loads(row['DATA'])['impressions']
        if temp_data == []: continue
        if temp_bid not in bid_dict:
            bid_dict[temp_bid] = []
        bid_dict[temp_bid].extend([mean(temp_data[:24])])

    fp.write('total\t'+str(len(bid_dict))+'\n')
    for bid in bid_dict:
        fp.write(str(bid)+'\t'+str(len(bid_dict[bid]))+'\t'+str(mean(bid_dict[bid]))+'\t'+str(std(bid_dict[bid]))+'\t')
        for data in bid_dict[bid]:
            fp.write(str(data)+'\t')
        fp.write('\n')
    fp.close()

def HowManyUser():
    cur = MydbExec(("SELECT TARGETED_USERS, LOCAL_STATUS FROM Campaigns WHERE 1",))
    userid_list = []
    good_userid_list = []
    bad_userid_list = []
    print 'record num: %d'%cur.rowcount
    for i in range(cur.rowcount):
        row = cur.fetchone()
        temp_user = row['TARGETED_USERS']
        if temp_user==None: continue
        if len(temp_user)==0: continue
        temp_user = temp_user.split(',')
        for userid in temp_user:
            userid_list.append(userid)
            if row['LOCAL_STATUS'] == 5:
                bad_userid_list.append(userid)
            else:
                good_userid_list.append(userid)
    print 'totaluserid: ', len(set(userid_list)), ' | gooduserid: ', len(set(good_userid_list)), ' | baduserid: ', len(set(bad_userid_list))

