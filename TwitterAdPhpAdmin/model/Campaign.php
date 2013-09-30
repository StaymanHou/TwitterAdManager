<?php
class Campaign
{
    private $fields;

    // initialize a User object
    public function __construct()
    {
        $this->fields = array('num' => 0,
                              'lst' => null);
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
    public static function getnum($fi_id=null, $local_status=null)
    {
        $num = 0;

        $query = 'SELECT COUNT(*) AS COUNT FROM Campaigns WHERE 1=1';
        if ($fi_id!=null) {
            $query .= sprintf(' AND FI_ID = %d',$fi_id);
        }
        if ($local_status!=null) {
            $query .= sprintf(' AND LOCAL_STATUS = %d',$local_status);
        }
        $result = mysql_query($query, $GLOBALS['DB']);
        if (mysql_num_rows($result))
        {
            $row = mysql_fetch_assoc($result);
            $num = $row['COUNT'];
        }
        mysql_free_result($result);

        return $num;
    }

    // return an object populated based on the record's user id
    public static function getlist($fi_id=null,$local_status=null)
    {
        $lst = array();

        $query = 'SELECT NAME, LOCAL_STATUS, ACTIVE, START_TIME, END_TIME, FI_ID, TOTAL_BUDGET, DAILY_BUDGET, MAX_BID, TARGETED_USERS, TARGETED_INTERESTS, LOCATIONS, PAC_TO_SIMILAR, GENDER, ACCELERATED_DELIVERY FROM Campaigns WHERE 1=1';
        if ($fi_id!=null) {
            $query .= sprintf(' AND FI_ID = %d',$fi_id);
        }
        if ($local_status!=null) {
            $query .= sprintf(' AND LOCAL_STATUS = %d',$local_status);
        }
        $query .= ' ORDER BY PK DESC LIMIT 300';
        $result = mysql_query($query, $GLOBALS['DB']);
        while ($row = mysql_fetch_assoc($result)) {
            array_push($lst, $row);
        }
        mysql_free_result($result);

        return $lst;
    }

    public static function killalive($fi_id=null)
    {
        $query = 'UPDATE `Campaigns` SET `LOCAL_STATUS`=4 WHERE (`LOCAL_STATUS`=2 OR `LOCAL_STATUS`=3)';
        if ($fi_id!=null) {
            $query .= sprintf(' AND FI_ID = %d',$fi_id);
        }
        mysql_query($query, $GLOBALS['DB']);
        return 0;
    }

    public static function reset()
    {
        $file = 'backups/twCampaign-' . time() . '.sql';
        mysql_query("SELECT * INTO OUTFILE '".$file."' FROM `Campaigns`");
        $query = "DELETE FROM `Campaigns`";
        mysql_query($query, $GLOBALS['DB']);
    }
}
?>
