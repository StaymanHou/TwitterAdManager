<?php
class Account
{
    private $PK;
    private $fields;

    // initialize a User object
    public function __construct()
    {
        $this->PK = null;
        $this->fields = array('FI_ID' => null,
                              'USERNAME' => null,
                              'PSWD' => null,
                              'ACTIVE' => false,
                              'BUDGET_LIMIT_THRESHOLD' => 5.0,
                              'POOR_ZSCORE_THRESHOLD' => 0.0,
                              'EFFECTIVE_DAYS' => 7,
                              'MAX_CAMPAIGN_NUM' => 200,
                              'USER_NUM_LOW' => 0,
                              'USER_NUM_HIGH' => 0,
                              'USER_PRIVATE_WEIGHT' => 0.0,
                              'INTST_NUM_LOW' => 0,
                              'INTST_NUM_HIGH' => 0,
                              'INTST_PRIVATE_WEIGHT' => 0.0,
                              'CNTRY_NUM_LOW' => 0,
                              'CNTRY_NUM_HIGH' => 0,
                              'CNTRY_PRIVATE_WEIGHT' => 0.0,
                              'BID_LOW' => 0.01,
                              'BID_HIGH' => 0.01,
                              'CMP_BUDGET' => 100.0,
                              'DLY_BUDGET' => 10.0,
                              'PTS' => true,
                              'GENDER' => 0,
                              'ACCELERATED_DELIVERY' => true,
                              'MONITOR_FINISHED_HOUR' => null,
                              'CONTROLLER_FINISHED_HOUR' => null,
                              'UPDATE_TIME DATETIME' => null,
                              'DELETED' => false);
    }

    // override magic method to retrieve properties
    public function __get($field)
    {
        if ($field == 'PK')
        {
            return $this->PK;
        }
        else 
        {
            return $this->fields[$field];
        }
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
    public static function getByPK($PK)
    {
        $acc = new Account();
        $query = sprintf("SELECT `FI_ID`, `USERNAME`, `ACTIVE`, `BUDGET_LIMIT_THRESHOLD`, `POOR_ZSCORE_THRESHOLD`, `EFFECTIVE_DAYS`, `MAX_CAMPAIGN_NUM`, `USER_NUM_LOW`, `USER_NUM_HIGH`, `USER_PRIVATE_WEIGHT`, `INTST_NUM_LOW`, `INTST_NUM_HIGH`, `INTST_PRIVATE_WEIGHT`, `CNTRY_NUM_LOW`, `CNTRY_NUM_HIGH`, `CNTRY_PRIVATE_WEIGHT`, `BID_LOW`, `BID_HIGH`, `CMP_BUDGET`, `DLY_BUDGET`, `PTS`, `GENDER`, `ACCELERATED_DELIVERY` FROM `Accounts` WHERE `PK` = %d",$PK);
        $result = mysql_query($query, $GLOBALS['DB']);

        if (mysql_num_rows($result))
        {
            $row = mysql_fetch_assoc($result);
            $acc->FI_ID = $row['FI_ID'];
            $acc->USERNAME = $row['USERNAME'];
            $acc->ACTIVE = $row['ACTIVE'];
            $acc->BUDGET_LIMIT_THRESHOLD = $row['BUDGET_LIMIT_THRESHOLD'];
            $acc->POOR_ZSCORE_THRESHOLD = $row['POOR_ZSCORE_THRESHOLD'];
            $acc->EFFECTIVE_DAYS = $row['EFFECTIVE_DAYS'];
            $acc->MAX_CAMPAIGN_NUM = $row['MAX_CAMPAIGN_NUM'];
            $acc->USER_NUM_LOW = $row['USER_NUM_LOW'];
            $acc->USER_NUM_HIGH = $row['USER_NUM_HIGH'];
            $acc->USER_PRIVATE_WEIGHT = $row['USER_PRIVATE_WEIGHT'];
            $acc->INTST_NUM_LOW = $row['INTST_NUM_LOW'];
            $acc->INTST_NUM_HIGH = $row['INTST_NUM_HIGH'];
            $acc->INTST_PRIVATE_WEIGHT = $row['INTST_PRIVATE_WEIGHT'];
            $acc->CNTRY_NUM_LOW = $row['CNTRY_NUM_LOW'];
            $acc->CNTRY_NUM_HIGH = $row['CNTRY_NUM_HIGH'];
            $acc->CNTRY_PRIVATE_WEIGHT = $row['CNTRY_PRIVATE_WEIGHT'];
            $acc->BID_LOW = $row['BID_LOW'];
            $acc->BID_HIGH = $row['BID_HIGH'];
            $acc->CMP_BUDGET = $row['CMP_BUDGET'];
            $acc->DLY_BUDGET = $row['DLY_BUDGET'];
            $acc->PTS = $row['PTS'];
            $acc->GENDER = $row['GENDER'];
            $acc->ACCELERATED_DELIVERY = $row['ACCELERATED_DELIVERY'];
            $acc->PK = $PK;
        }
        mysql_free_result($result);

        return $acc;
    }

    // return an object populated based on the record's user id 
    public static function getlist()
    {
        $lst = array();

        $query = sprintf("SELECT `PK`, `FI_ID`, `USERNAME`, `ACTIVE`, `BUDGET_LIMIT_THRESHOLD`, `ACC_BUDGET`, `ACC_BUDGET_REMAIN`, `POOR_ZSCORE_THRESHOLD`, `EFFECTIVE_DAYS`, `MAX_CAMPAIGN_NUM`, `BID_LOW`, `BID_HIGH` FROM `Accounts` WHERE `DELETED` = FALSE ORDER BY PK DESC");
        $result = mysql_query($query, $GLOBALS['DB']);
        while ($row = mysql_fetch_assoc($result)) {
            array_push($lst, $row);
        }
        mysql_free_result($result);

        return $lst;
    }

    public static function getactivenum()
    {
        $num = 0;

        $query = "SELECT COUNT(*) AS COUNT FROM `Accounts` WHERE `ACTIVE` = TRUE AND `DELETED` = FALSE";
        $result = mysql_query($query, $GLOBALS['DB']);
        if (mysql_num_rows($result))
        {
            $row = mysql_fetch_assoc($result);
            $num = $row['COUNT'];
        }
        return $num;
    }

    public static function gettotalnum()
    {
        $num = 0;

        $query = "SELECT COUNT(*) AS COUNT FROM `Accounts` WHERE `DELETED` = FALSE";
        $result = mysql_query($query, $GLOBALS['DB']);
        if (mysql_num_rows($result))
        {
            $row = mysql_fetch_assoc($result);
            $num = $row['COUNT'];
        }
        return $num;
    }

    public function save($withpw=false,$updatetime=false)
    {
        if ($this->PK!=null)
        {
            if ($withpw) {
                $query = sprintf('UPDATE `Accounts` SET USERNAME = "%s", `PSWD` = DES_ENCRYPT("%s","%s"), ACTIVE = %s, BUDGET_LIMIT_THRESHOLD = %f, POOR_ZSCORE_THRESHOLD = %f, EFFECTIVE_DAYS = %d, MAX_CAMPAIGN_NUM = %d, USER_NUM_LOW = %d, USER_NUM_HIGH = %d, USER_PRIVATE_WEIGHT = %f, INTST_NUM_LOW = %d, INTST_NUM_HIGH = %d, INTST_PRIVATE_WEIGHT = %f, CNTRY_NUM_LOW = %d, CNTRY_NUM_HIGH = %d, CNTRY_PRIVATE_WEIGHT = %f, BID_LOW = %f, BID_HIGH = %f, CMP_BUDGET = %f, DLY_BUDGET = %f, PTS = %s, GENDER = %d, ACCELERATED_DELIVERY = %s WHERE PK = %d',
                    $this->USERNAME,
                    $this->PSWD,
                    DB_KEY,
                    $this->ACTIVE?'True':'False',
                    $this->BUDGET_LIMIT_THRESHOLD,
                    $this->POOR_ZSCORE_THRESHOLD,
                    $this->EFFECTIVE_DAYS,
                    $this->MAX_CAMPAIGN_NUM,
                    $this->USER_NUM_LOW,
                    $this->USER_NUM_HIGH,
                    $this->USER_PRIVATE_WEIGHT,
                    $this->INTST_NUM_LOW,
                    $this->INTST_NUM_HIGH,
                    $this->INTST_PRIVATE_WEIGHT,
                    $this->CNTRY_NUM_LOW,
                    $this->CNTRY_NUM_HIGH,
                    $this->CNTRY_PRIVATE_WEIGHT,
                    $this->BID_LOW,
                    $this->BID_HIGH,
                    $this->CMP_BUDGET,
                    $this->DLY_BUDGET,
                    $this->PTS?'True':'False',
                    $this->GENDER,
                    $this->ACCELERATED_DELIVERY?'True':'False',
                    $this->PK);
                mysql_query($query, $GLOBALS['DB']);
            } else {
                if ($updatetime)
                {
                    $query = sprintf('UPDATE `Accounts` SET USERNAME = "%s", ACTIVE = %s, BUDGET_LIMIT_THRESHOLD = %f, POOR_ZSCORE_THRESHOLD = %f, EFFECTIVE_DAYS = %d, MAX_CAMPAIGN_NUM = %d, USER_NUM_LOW = %d, USER_NUM_HIGH = %d, USER_PRIVATE_WEIGHT = %f, INTST_NUM_LOW = %d, INTST_NUM_HIGH = %d, INTST_PRIVATE_WEIGHT = %f, CNTRY_NUM_LOW = %d, CNTRY_NUM_HIGH = %d, CNTRY_PRIVATE_WEIGHT = %f, BID_LOW = %f, BID_HIGH = %f, CMP_BUDGET = %f, DLY_BUDGET = %f, PTS = %s, GENDER = %d, ACCELERATED_DELIVERY = %s, UPDATE_TIME = NOW() WHERE PK = %d',
                        $this->USERNAME,
                        $this->ACTIVE?'True':'False',
                        $this->BUDGET_LIMIT_THRESHOLD,
                        $this->POOR_ZSCORE_THRESHOLD,
                        $this->EFFECTIVE_DAYS,
                        $this->MAX_CAMPAIGN_NUM,
                        $this->USER_NUM_LOW,
                        $this->USER_NUM_HIGH,
                        $this->USER_PRIVATE_WEIGHT,
                        $this->INTST_NUM_LOW,
                        $this->INTST_NUM_HIGH,
                        $this->INTST_PRIVATE_WEIGHT,
                        $this->CNTRY_NUM_LOW,
                        $this->CNTRY_NUM_HIGH,
                        $this->CNTRY_PRIVATE_WEIGHT,
                        $this->BID_LOW,
                        $this->BID_HIGH,
                        $this->CMP_BUDGET,
                        $this->DLY_BUDGET,
                        $this->PTS?'True':'False',
                        $this->GENDER,
                        $this->ACCELERATED_DELIVERY?'True':'False',
                        $this->PK);
                    mysql_query($query, $GLOBALS['DB']);
                } else {
                    $query = sprintf('UPDATE `Accounts` SET USERNAME = "%s", ACTIVE = %s, BUDGET_LIMIT_THRESHOLD =%f, POOR_ZSCORE_THRESHOLD = %f, EFFECTIVE_DAYS = %d, MAX_CAMPAIGN_NUM = %d, USER_NUM_LOW = %d, USER_NUM_HIGH = %d, USER_PRIVATE_WEIGHT = %f, INTST_NUM_LOW = %d, INTST_NUM_HIGH = %d, INTST_PRIVATE_WEIGHT = %f, CNTRY_NUM_LOW = %d, CNTRY_NUM_HIGH = %d, CNTRY_PRIVATE_WEIGHT = %f, BID_LOW = %f, BID_HIGH = %f, CMP_BUDGET = %f, DLY_BUDGET = %f, PTS = %s, GENDER = %d, ACCELERATED_DELIVERY = %s WHERE PK = %d',
                        $this->USERNAME,
                        $this->ACTIVE?'True':'False',
                        $this->BUDGET_LIMIT_THRESHOLD,
                        $this->POOR_ZSCORE_THRESHOLD,
                        $this->EFFECTIVE_DAYS,
                        $this->MAX_CAMPAIGN_NUM,
                        $this->USER_NUM_LOW,
                        $this->USER_NUM_HIGH,
                        $this->USER_PRIVATE_WEIGHT,
                        $this->INTST_NUM_LOW,
                        $this->INTST_NUM_HIGH,
                        $this->INTST_PRIVATE_WEIGHT,
                        $this->CNTRY_NUM_LOW,
                        $this->CNTRY_NUM_HIGH,
                        $this->CNTRY_PRIVATE_WEIGHT,
                        $this->BID_LOW,
                        $this->BID_HIGH,
                        $this->CMP_BUDGET,
                        $this->DLY_BUDGET,
                        $this->PTS?'True':'False',
                        $this->GENDER,
                        $this->ACCELERATED_DELIVERY?'True':'False',
                        $this->PK);
                    mysql_query($query, $GLOBALS['DB']);
                }
            }
        }
        else
        {
            $query = sprintf('INSERT INTO `Accounts` (USERNAME, `PSWD`, FI_ID, ACTIVE, BUDGET_LIMIT_THRESHOLD, POOR_ZSCORE_THRESHOLD, EFFECTIVE_DAYS, MAX_CAMPAIGN_NUM, USER_NUM_LOW, USER_NUM_HIGH, USER_PRIVATE_WEIGHT, INTST_NUM_LOW, INTST_NUM_HIGH, INTST_PRIVATE_WEIGHT, CNTRY_NUM_LOW, CNTRY_NUM_HIGH, CNTRY_PRIVATE_WEIGHT, BID_LOW, BID_HIGH, CMP_BUDGET, DLY_BUDGET, PTS, GENDER, ACCELERATED_DELIVERY, UPDATE_TIME
) VALUES ("%s", DES_ENCRYPT("%s","%s"), %d, %s, %f, %f, %d, %d, %d, %d, %f, %d, %d, %f, %d, %d, %f, %f, %f, %f, %f, %s, %d, %s, NOW())',
                $this->USERNAME,
                $this->PSWD,
                DB_KEY,
                $this->FI_ID,
                $this->ACTIVE?'True':'False',
                $this->BUDGET_LIMIT_THRESHOLD,
                $this->POOR_ZSCORE_THRESHOLD,
                $this->EFFECTIVE_DAYS,
                $this->MAX_CAMPAIGN_NUM,
                $this->USER_NUM_LOW,
                $this->USER_NUM_HIGH,
                $this->USER_PRIVATE_WEIGHT,
                $this->INTST_NUM_LOW,
                $this->INTST_NUM_HIGH,
                $this->INTST_PRIVATE_WEIGHT,
                $this->CNTRY_NUM_LOW,
                $this->CNTRY_NUM_HIGH,
                $this->CNTRY_PRIVATE_WEIGHT,
                $this->BID_LOW,
                $this->BID_HIGH,
                $this->CMP_BUDGET,
                $this->DLY_BUDGET,
                $this->PTS?'True':'False',
                $this->GENDER,
                $this->ACCELERATED_DELIVERY?'True':'False');
            mysql_query($query, $GLOBALS['DB']);
            $this->PK = mysql_insert_id($GLOBALS['DB']);
        }
        return 0;
    }

    public static function toggleactive($PK)
    {
        $query = sprintf('UPDATE `Accounts` SET `ACTIVE`=(!`ACTIVE`) WHERE PK = %d', $PK);
        mysql_query($query, $GLOBALS['DB']);
        return 0;
    }

    public static function setdelete($PK)
    {
        $query = sprintf('UPDATE `Accounts` SET `DELETED`=True, `ACTIVE`=False WHERE PK = %d', $PK);
        mysql_query($query, $GLOBALS['DB']);
        return 0;
    }

    public static function setbudget($Budget, $PK)
    {
        $query = sprintf('UPDATE `Accounts` SET ACC_BUDGET = %f, ACC_BUDGET_REMAIN = %f WHERE PK = %d', $Budget, $Budget, $PK);
        mysql_query($query, $GLOBALS['DB']);
        return 0;
    }

    public static function addbudget($Budget, $PK)
    {
        $query = sprintf('UPDATE `Accounts` SET ACC_BUDGET = ACC_BUDGET+%f, ACC_BUDGET_REMAIN = ACC_BUDGET_REMAIN+%f WHERE PK = %d', $Budget, $Budget, $PK);
        mysql_query($query, $GLOBALS['DB']);
        return 0;
    }
}
?>
