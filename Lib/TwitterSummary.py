from DB import DB

class TwitterSummary(object):
    """A Twitter Summary object. Contains fi_id, data and etc. 
        It is corresponding to TwitterAccount through :attr:`fi_id`.
        It uses :class:`Lib.DB.DB`.
    """

    pk = 0
    fi_id = None
    period_start = None
    period_end = None
    total_spend = 0.0
    total_impressions = 0
    total_engagements = 0
    new_spend = 0
    new_impressions = 0
    new_engagements = 0

    def __init__(self):
        super(TwitterSummary, self).__init__()

    def get_last(fi_id):
        """Return the latest Summary object of the give fi_id account.
        """
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
        """INSERT the new Summary.
        """
        db = DB()
        query_tuple = ("INSERT INTO "\
                "Summaries(FI_ID, PERIOD_START, PERIOD_END, "\
                "TOTAL_SPEND, TOTAL_IMPRESSIONS, TOTAL_ENGAGEMENTS, "\
                "NEW_SPEND, NEW_IMPRESSIONS, NEW_ENGAGEMENTS) "\
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (self.fi_id, self.period_start, self.period_end,
                self.total_spend, self.total_impressions, self.total_engagements,
                self.new_spend, self.new_impressions, self.new_engagements))
        cur = db.execute(query_tuple)
        self.pk = cur.lastrowid
