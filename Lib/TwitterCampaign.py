import json
from DB import DB

class TwitterCampaign(object):
    """A Twitter Campaign object. Contains id, name,
        status, data and etc. It uses :class:`Lib.DB.DB`.
        \n..note::
        \n\tself.data is stored as a JSON object in database
    """

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
    data = {'spend':[],'total_spend':0,
            'impressions':[],'total_impressions':0,
            'engagements':[],'total_engagements':0}
    targeted_users = ''
    targeted_interests = ''
    locations = ''
    pac_to_similar = True
    gender = 0
    accelerated_delivery = 1

    def __init__(self):
        super(TwitterCampaign, self).__init__()
        self.pk = 0
        self.id = 0
        self.name = ''
        self.local_status = None
        self.active = False
        self.start_time = None
        self.end_time = None
        self.fi_id = 0
        self.total_budget = 100
        self.daily_budget = 10
        self.max_bid = 0.01
        self.data = {'spend':[],'total_spend':0,
                     'impressions':[],'total_impressions':0,
                     'engagements':[],'total_engagements':0}
        self.targeted_users = ''
        self.targeted_interests = ''
        self.locations = ''
        self.pac_to_similar = True
        self.gender = 0
        self.accelerated_delivery = 1

    def get_alive_createpending_num(fi_id):
        """Return the number of the Campaigns of the account which are alive or 
            create_pending.
        """
        db = DB()
        query_tuple = ("SELECT COUNT(*) AS COUNT FROM Campaigns WHERE (LOCAL_STATUS = 2 OR LOCAL_STATUS = 3) AND FI_ID=%s",fi_id)
        cur = db.execute(query_tuple)
        if cur.rowcount == 0:
            raise Exception('TwitterCampaign', 'No such user %d'%fi_id)
        return cur.fetchone()['COUNT']

    get_alive_createpending_num = staticmethod(get_alive_createpending_num)

    def get_list(fi_id, local_status=None):
        """Return a list of :class:`Lib.TwitterCampaign.TwitterCampaign` of a give fi_id.
            local_status can be specified. 
        """
        db = DB()
        query_tuple = ("DELETE FROM `Campaigns` WHERE `ID`=0 AND `LOCAL_STATUS`=4", ())
        db.execute(query_tuple)
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
            if row['DATA']!=None and row['DATA']!='':
                camp.data = json.loads(row['DATA'])
            camp.targeted_users = row['TARGETED_USERS']
            camp.targeted_interests = row['TARGETED_INTERESTS']
            camp.locations = row['LOCATIONS']
            camp.pac_to_similar = row['PAC_TO_SIMILAR']
            camp.gender = row['GENDER']
            camp.accelerated_delivery = row['ACCELERATED_DELIVERY']
            camp_list.append(camp)
        return camp_list

    get_list = staticmethod(get_list)

    def save(self):
        """Save the campaign to database.
            If it has non-zeor :attr:`pk`, it will do UPDATE.
            Otherwise, do INSERT.
        """
        db = DB()
        query_tuple = None
        if self.pk == 0:
            query_tuple = ("INSERT INTO "\
                    "Campaigns(ID, NAME, LOCAL_STATUS, ACTIVE, "\
                    "START_TIME, END_TIME, FI_ID, TOTAL_BUDGET, "\
                    "DAILY_BUDGET, MAX_BID, DATA, TARGETED_USERS, "\
                    "TARGETED_INTERESTS, LOCATIONS, PAC_TO_SIMILAR, "\
                    "GENDER, ACCELERATED_DELIVERY) "\
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (self.id, self.name, self.local_status, self.active,
                    self.start_time, self.end_time, self.fi_id, self.total_budget,
                    self.daily_budget, self.max_bid, json.JSONEncoder().encode(self.data), self.targeted_users,
                    self.targeted_interests, self.locations, self.pac_to_similar,
                    self.gender, self.accelerated_delivery))
        else:
            query_tuple = ("UPDATE Campaigns SET "\
                    "ID=%s, NAME=%s, LOCAL_STATUS=%s, ACTIVE=%s, "\
                    "START_TIME=%s, END_TIME=%s, FI_ID=%s, TOTAL_BUDGET=%s, "\
                    "DAILY_BUDGET=%s, MAX_BID=%s, DATA=%s, TARGETED_USERS=%s, "\
                    "TARGETED_INTERESTS=%s, LOCATIONS=%s, PAC_TO_SIMILAR=%s, "\
                    "GENDER=%s, ACCELERATED_DELIVERY=%s "\
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
