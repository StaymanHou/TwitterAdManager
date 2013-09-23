from DB import DB

class TwitterSummary(object):
    """docstring for TwitterSummary"""

    pk = 0
    fi_id = None
    period_start = None
    period_end = None
    total_spend = None
    total_impressions = None
    total_engagements = None
    new_spend = None
    new_impressions = None
    new_engagements = None

    def __init__(self):
        super(TwitterSummary, self).__init__()

    def save(self):
        db = DB()
        query_tuple = None
        query_tuple = ("INSERT INTO "/
                "Summaries(FI_ID, PERIOD_START, PERIOD_END, "/
                "TOTAL_SPEND, TOTAL_IMPRESSIONS, TOTAL_ENGAGEMENTS, "/
                "NEW_SPEND, NEW_IMPRESSIONS, NEW_ENGAGEMENTS"/
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (self.fi_id, self.period_start, self.period_end,
                self.total_spend, total_impressions, total_engagements,
                new_spend, new_impressions, new_engagements))
        cur = db.execute(query_tuple)
        self.pk = cur.lastrowid
