import json
from DB import DB

class TwitterCampaign(object):
    """docstring for TwitterCampaign"""

    pk = 0
    id = 0
    name = ''
    local_status = None
    active = False
    start_time = None
    end_time = None
    fi_id = 0
    total_budget = 100
    daily_budget = 10
    max_bid = 0.01
    data = ''
    targeted_users = ''
    targeted_interests = ''
    pac_to_similar = True
    gender = 0
    accelerated_delivery = 1

    def __init__(self):
        super(TwitterCampaign, self).__init__()

    def get_list(fi_id, local_status=None):
        db = DB()
        query_tuple = None
        if local_status is None:
            query_tuple = ("SELECT * FROM `Campaigns` WHERE `FI_ID`=%s", (fi_id))
        else:
            query_tuple = ("SELECT * FROM `Campaigns` WHERE `FI_ID`=%s AND LOCAL_STATUS=%s", (fi_id, local_status))
        cur = db.execute(query_tuple)
        camp_list = []
        rows = cur.fetchall()
        for row in rows:
            camp = TwitterCampaign()
            camp.pk = row['PK']
            camp.id = row['ID']
            camp.name = row['NAME']
            camp.local_status = row['LOCAL_STATUS']
            camp.active = row['ACTIVE']
            camp.start_time = row['START_TIME']
            camp.end_time = row['END_TIME']
            camp.fi_id = row['FI_ID']
            camp.total_budget = row['TOTAL_BUDGET']
            camp.daily_budget = row['DAILY_BUDGET']
            camp.max_bid = row['MAX_BID']
            camp.data = row['DATA']
            camp.targeted_users = row['TARGETED_USERS']
            camp.targeted_interests = row['TARGETED_INTERESTS']
            camp.pac_to_similar = row['PAC_TO_SIMILAR']
            camp.gender = row['GENDER']
            camp.accelerated_delivery = row['ACCELERATED_DELIVERY']
            camp_list.append(camp)
        return camp_list

    get_list = staticmethod(get_list)

    def save(self):
        db = DB()
        query_tuple = None
        if self.pk == 0:
            query_tuple = ("INSERT INTO "/
                    "Campaigns(ID, NAME, LOCAL_STATUS, ACTIVE, "/
                    "START_TIME, END_TIME, FI_ID, TOTAL_BUDGET, "/
                    "DAILY_BUDGET, MAX_BID, DATA, TARGETED_USERS, "/
                    "TARGETED_INTERESTS, LOCATIONS, PAC_TO_SIMILAR, "/
                    "GENDER, ACCELERATED_DELIVERY) "/
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (self.id, self.name, self.local_status, self.active,
                    self.start_time, self.end_time, self.fi_id, self.total_budget,
                    self.daily_budget, self.max_bid, json.JSONEncoder().encode(self.data), self.targeted_users,
                    self.targeted_interests, self.locations, self.pac_to_similar,
                    self.gender, self.accelerated_delivery))
        else:
            query_tuple = ("UPDATE Campaigns SET "/
                    "ID=%s, NAME=%s, LOCAL_STATUS=%s, ACTIVE=%s, "/
                    "START_TIME=%s, END_TIME=%s, FI_ID=%s, TOTAL_BUDGET=%s, "/
                    "DAILY_BUDGET=%s, MAX_BID=%s, DATA=%s, TARGETED_USERS=%s, "/
                    "TARGETED_INTERESTS=%s, LOCATIONS=%s, PAC_TO_SIMILAR=%s, "/
                    "GENDER=%s, ACCELERATED_DELIVERY=%s "/
                    "WHERE PK=%s",
                    (self.id, self.name, self.local_status, self.active,
                    self.start_time, self.end_time, self.fi_id, self.total_budget,
                    self.daily_budget, self.max_bid, json.JSONEncoder().encode(self.data), self.targeted_users,
                    self.targeted_interests, self.locations, self.pac_to_similar,
                    self.gender, self.accelerated_delivery,
                    self.pk))
        cur = db.execute(query_tuple)
        if self.pk == 0:
            self.pk = cur.lastrowid
