from MyDict import COUNTRY_ID_DICT,INTEREST_ID_DICT
from MyFunction import Username2Userid, file2list, randpick
from TwitterCampaign import TwitterCampaign
from LocalStatus import LocalStatus
from random import randint
import os

list_file_dir = 'list_files/'
user_list_name = 'user_list.txt'
intst_list_name = 'intst_list.txt'
cntry_list_name = 'cntry_list.txt'

def crtpd2refillcmp(account, generate_num):
    if generate_num<=0: return None
    prefix = '%s_'%account.username
    account.user_private_weight = min(1,max(0,account.user_private_weight))
    account.intst_private_weight = min(1,max(0,account.intst_private_weight))
    account.cntry_private_weight = min(1,max(0,account.cntry_private_weight))
    if not os.path.exists(list_file_dir):
        os.makedirs(list_file_dir)
    user_common_raw_list = file2list(list_file_dir+'common_'+user_list_name)
    user_private_raw_list = file2list(list_file_dir+prefix+user_list_name)
    intst_common_raw_list = file2list(list_file_dir+'common_'+intst_list_name)
    intst_private_raw_list = file2list(list_file_dir+prefix+intst_list_name)
    cntry_common_raw_list = file2list(list_file_dir+'common_'+cntry_list_name)
    cntry_private_raw_list = file2list(list_file_dir+prefix+cntry_list_name)
    for i in range(generate_num):
        ####### randomly choose intst_num, user_num, cntry_num, bid
        user_num = randint(account.user_num_low, account.user_num_high)
        user_private_num = int(user_num*account.user_private_weight)
        user_common_num = user_num - user_private_num
        intst_num = randint(account.intst_num_low, account.intst_num_high)
        intst_private_num = int(intst_num*account.intst_private_weight)
        intst_common_num = intst_num - intst_private_num
        cntry_num = randint(account.cntry_num_low, account.cntry_num_high)
        cntry_private_num = int(cntry_num*account.cntry_private_weight)
        cntry_common_num = cntry_num - cntry_private_num
        bid = float(randint(int(account.bid_low*100),int(account.bid_high*100)))/100
        ####### vvv generate user field vvv ########
        title_user = ''
        targeted_users = ''
        pick_list = []
        if len(user_private_raw_list)>user_private_num:
            pick_list = randpick(user_private_num,user_private_raw_list)
        else:
            pick_list = user_private_raw_list
        if len(user_common_raw_list)>user_common_num:
            pick_list.extend(randpick(user_common_num,user_common_raw_list))
        else:
            pick_list.extend(user_common_raw_list)
        if len(pick_list)==0:
            title_user = '000User'
        elif len(pick_list)==1:
            title_user = '001'+pick_list[0]
        else:
            title_user = '%03duser_'%len(pick_list)+pick_list[0]
        title_user = title_user[:15]
        target_user_id = []
        for username in pick_list:
            t_userid = Username2Userid(username)
            if type(t_userid) != unicode:
                continue
            target_user_id.append(t_userid)
        for t_userid in target_user_id:
            targeted_users += t_userid+','
        targeted_users = targeted_users[:-1]
        ####### vvv generate interest field vvv ########
        title_interest = ''
        targeted_interests = ''
        pick_list = []
        if len(intst_private_raw_list)>intst_private_num:
            pick_list = randpick(intst_private_num,intst_private_raw_list)
        else:
            pick_list = intst_private_raw_list
        if len(intst_common_raw_list)>intst_common_num:
            pick_list.extend(randpick(intst_common_num,intst_common_raw_list))
        else:
            pick_list.extend(intst_common_raw_list)
        if len(pick_list)==0:
            title_interest = '000Intst'
        elif len(pick_list)==1:
            title_interest = '001'+pick_list[0]
        else:
            title_interest = '%03dintst_'%len(pick_list)+pick_list[0]
        title_interest = title_interest[:15]
        target_interest_id = []
        for interest in pick_list:
            if interest.lower() not in INTEREST_ID_DICT:
                continue
            t_intstid = INTEREST_ID_DICT[interest.lower()]
            target_interest_id.append(t_intstid)
        for t_intstid in target_interest_id:
            targeted_interests += t_intstid+','
        targeted_interests = targeted_interests[:-1]
        ####### vvv generate location field vvv ########
        title_country = ''
        locations = ''
        pick_list = []
        if len(cntry_private_raw_list)>cntry_private_num:
            pick_list = randpick(cntry_private_num,cntry_private_raw_list)
        else:
            pick_list = cntry_private_raw_list
        if len(cntry_common_raw_list)>cntry_common_num:
            pick_list.extend(randpick(cntry_common_num,cntry_common_raw_list))
        else:
            pick_list.extend(cntry_common_raw_list)
        if len(pick_list)==0:
            title_country = '000Worldwide'
        elif len(pick_list)==1:
            title_country = '001'+pick_list[0]
        else:
            title_country = '%03dcntry_'%len(pick_list)+pick_list[0]
        title_country = title_country[:15]
        target_location_id = []
        for location in pick_list:
            if location.lower() not in COUNTRY_ID_DICT:
                continue
            t_cntryid = COUNTRY_ID_DICT[location.lower()]
            target_location_id.append(t_cntryid)
        for t_cntryid in target_location_id:
            locations += t_cntryid+','
        locations = locations[:-1]
        ######### vvvv create pending in db vvvv ########
        campaign = TwitterCampaign()
        campaign.name = title_interest+'_'+title_user+'_'+title_country
        campaign.local_status = LocalStatus.TitletoPK['CreatePending']
        campaign.fi_id = account.fi_id
        campaign.total_budget = account.cmp_budget
        campaign.daily_budget = account.daily_budget
        campaign.max_bid = bid
        campaign.data = {'spend':[],'total_spend':0,'impressions':[],'total_impressions':0,'engagements':[],'total_engagements':0}
        campaign.targeted_users = targeted_users
        campaign.targeted_interests = targeted_interests
        campaign.locations = locations
        campaign.pac_to_similar = account.pts
        campaign.gender = account.gender
        campaign.accelerated_delivery = account.accelerated_delivery
        campaign.save()
    return generate_num
