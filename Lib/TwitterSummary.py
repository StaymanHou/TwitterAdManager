from DB import DB

class TwitterSummary(object):
    """docstring for TwitterSummary"""

    pk = 0
    fi_id = None
    period_start = None
    period_end = None
    total_spend = 0
    total_impressions = 0
    total_engagements = 0
    new_spend = 0
    new_impressions = 0
    new_engagements = 0

    def __init__(self):
        super(TwitterSummary, self).__init__()

    def get_last(fi_id):
        db = DB()
        query_tuple = ("SELECT * FROM Summaries WHERE FI_ID=%s ORDER BY PK DESC LIMIT 1",fi_id)
        cur = db.execute(query_tuple)
        summary = TwitterSummary()
        summary.fi_id = fi_id
        if cur.rowcount:
            row = cur.fetchone()
            summary.period_start = row['PERIOD_START']
            summary.period_end = row['PERIOD_END']
            summary.total_spend = row['TOTAL_SPEND']
            summary.total_impressions = row['TOTAL_IMPRESSIONS']
            summary.total_engagements = row['TOTAL_ENGAGEMENTS']
            summary.new_spend = row['NEW_SPEND']
            summary.new_impressions = row['NEW_IMPRESSIONS']
            summary.new_engagements = row['NEW_ENGAGEMENTS']
        return summary

    get_last = staticmethod(get_last)

    def save(self):
        db = DB()
        query_tuple = ("INSERT INTO "\
                "Summaries(FI_ID, PERIOD_START, PERIOD_END, "\
                "TOTAL_SPEND, TOTAL_IMPRESSIONS, TOTAL_ENGAGEMENTS, "\
                "NEW_SPEND, NEW_IMPRESSIONS, NEW_ENGAGEMENTS"\
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (self.fi_id, self.period_start, self.period_end,
                self.total_spend, total_impressions, total_engagements,
                new_spend, new_impressions, new_engagements))
        cur = db.execute(query_tuple)
        self.pk = cur.lastrowid
