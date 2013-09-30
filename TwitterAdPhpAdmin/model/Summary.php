<?php
class Summary
{
    private $fields;

    // initialize a User object
    public function __construct()
    {
        $this->fields = array('FI_ID' => null,
                              'start' => null,
                              'end' => null,
                              'imp' => 0,
                              'eng' => 0,
                              'spd' => 0);
    }

    // override magic method to retrieve properties
    public function __get($field)
    {
        return $this->fields[$field];
    }

    // override magic method to set properties
    public function __set($field, $value)
    {
        if (array_key_exists($field, $this->fields))
        {
            $this->fields[$field] = $value;
        }
    }

    // return an object populated based on the record's user id
    public static function gettotal($start=null,$end=null,$fi_id=null)
    {
        $sm = new Summary();

        if ($fi_id==null) {
            if ($end==null) {
                $query = 'SELECT DISTINCT PERIOD_END FROM Summaries ORDER BY PERIOD_END DESC LIMIT 1';
                $result = mysql_query($query, $GLOBALS['DB']);
                if (mysql_num_rows($result)) {
                    $row = mysql_fetch_assoc($result);
                    $end = $row['PERIOD_END'];
                    $end = strtotime($end);
                }
                mysql_free_result($result);
            }
            $query = sprintf("SELECT TOTAL_IMPRESSIONS, TOTAL_ENGAGEMENTS, TOTAL_SPEND FROM Summaries INNER JOIN Accounts
ON Summaries.FI_ID=Accounts.FI_ID WHERE ACTIVE = TRUE AND PERIOD_END = '%s'",date('Y-m-d H:i:s',$end));
            $result = mysql_query($query, $GLOBALS['DB']);
            $imp_end = 0;
            $eng_end = 0;
            $spd_end = 0;
            while ($row = mysql_fetch_assoc($result)) {
                $imp_end += floatval($row['TOTAL_IMPRESSIONS']);
                $eng_end += floatval($row['TOTAL_ENGAGEMENTS']);
                $spd_end += floatval($row['TOTAL_SPEND']);
            }
            mysql_free_result($result);

            if ($start==null) {
                $imp_start = 0;
                $eng_start = 0;
                $spd_start = 0;
            } else {
                $query = sprintf("SELECT TOTAL_IMPRESSIONS, TOTAL_ENGAGEMENTS, TOTAL_SPEND FROM Summaries INNER JOIN Accounts
ON Summaries.FI_ID=Accounts.FI_ID WHERE ACTIVE = TRUE AND PERIOD_END = '%s'",date('Y-m-d H:i:s',$start));
                $result = mysql_query($query, $GLOBALS['DB']);
                $imp_start = 0;
                $eng_start = 0;
                $spd_start = 0;
                while ($row = mysql_fetch_assoc($result)) {
                    $imp_start += floatval($row['TOTAL_IMPRESSIONS']);
                    $eng_start += floatval($row['TOTAL_ENGAGEMENTS']);
                    $spd_start += floatval($row['TOTAL_SPEND']);
                }
                mysql_free_result($result);
            }
        } else {
            $query = sprintf('SELECT TOTAL_IMPRESSIONS, TOTAL_ENGAGEMENTS, TOTAL_SPEND FROM Summaries WHERE FI_ID = %d ',$fi_id);
            if ($end==null) {
                $query .= 'ORDER BY PERIOD_END DESC ';
            } else {
                $query .= sprintf("AND PERIOD_END = '%s' ",date('Y-m-d H:i:s',$end));
            }
            $query .= 'LIMIT 1';
            $result = mysql_query($query, $GLOBALS['DB']);
            $imp_end = 0;
            $eng_end = 0;
            $spd_end = 0;
            if (mysql_num_rows($result))
            {
                $row = mysql_fetch_assoc($result);
                $imp_end = $row['TOTAL_IMPRESSIONS'];
                $eng_end = $row['TOTAL_ENGAGEMENTS'];
                $spd_end = $row['TOTAL_SPEND'];
            }
            mysql_free_result($result);

            $query .= 'LIMIT 1';
            if ($start==null) {
                $imp_start = 0;
                $eng_start = 0;
                $spd_start = 0;
            } else {
                $query = sprintf("SELECT TOTAL_IMPRESSIONS, TOTAL_ENGAGEMENTS, TOTAL_SPEND FROM Summaries WHERE FI_ID = %d AND PERIOD_END = '%s' LIMIT 1",$fi_id,date('Y-m-d H:i:s',$start));
                $result = mysql_query($query, $GLOBALS['DB']);
                $imp_start = 0;
                $eng_start = 0;
                $spd_start = 0;
                if (mysql_num_rows($result))
                {
                    $row = mysql_fetch_assoc($result);
                    $imp_start = $row['TOTAL_IMPRESSIONS'];
                    $eng_start = $row['TOTAL_ENGAGEMENTS'];
                    $spd_start = $row['TOTAL_SPEND'];
                }
                mysql_free_result($result);
            }
        }

        $sm->FI_ID = $fi_id;
        $sm->start = $start;
        $sm->end = $end;
        $sm->imp = $imp_end - $imp_start;
        $sm->eng = $eng_end - $eng_start;
        $sm->spd = $spd_end - $spd_start;

        return $sm;
    }

    // return an object populated based on the record's user id
    public static function getlist($start,$end,$fi_id=null)
    {
        if ($fi_id==null) {
            $query = sprintf("SELECT SUM(NEW_IMPRESSIONS) AS NEW_IMPRESSIONS, SUM(NEW_ENGAGEMENTS) AS NEW_ENGAGEMENTS, SUM(NEW_SPEND) AS NEW_SPEND, PERIOD_END FROM Summaries WHERE PERIOD_END > '%s' AND PERIOD_END <= '%s' GROUP BY PERIOD_END ORDER BY PERIOD_END DESC",date('Y-m-d H:i:s',$start),date('Y-m-d H:i:s',$end));
        } else {
            $query = sprintf("SELECT NEW_IMPRESSIONS, NEW_ENGAGEMENTS, NEW_SPEND, PERIOD_END FROM Summaries WHERE FI_ID = %d AND PERIOD_END > '%s' AND PERIOD_END <= '%s' ORDER BY PERIOD_END ASC",$fi_id,date('Y-m-d H:i:s',$start),date('Y-m-d H:i:s',$end));
        }
        $result = mysql_query($query, $GLOBALS['DB']);

        return $result;
    }

    public static function reset()
    {
        $file = 'backups/twSummary-' . time() . '.sql';
        mysql_query("SELECT * INTO OUTFILE '".$file."' FROM Summaries");
        $query = "DELETE FROM Summaries";
        mysql_query($query, $GLOBALS['DB']);
    }
}
?>
