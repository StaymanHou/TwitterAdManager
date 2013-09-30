<?php
class MainConf
{
    private $PK;     // user id
    private $fields;  // other record fields

    // initialize a User object
    public function __construct()
    {
        $this->PK = null;
        $this->fields = array('CONF_TITLE' => '',
                              'MAX_MONITOR_THREAD' => 0,
                              'MON_LOAD_ITERATION' => 0,
                              'MON_CHECK_ITERATION' => 0,
                              'MON_TIMEOUT_LIMIT' => 0,
                              'MON_INIT_RETRY_WAITING_TIME' => 0,
                              'MON_INIT_RETRY_COMMON_RATIO' => 0);
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
    public static function get()
    {
        $mc = new MainConf();

        $query = 'SELECT `CONF_TITLE`, `MAX_MONITOR_THREAD`, `MON_LOAD_ITERATION`, `MON_CHECK_ITERATION`, `MON_TIMEOUT_LIMIT`, `MON_INIT_RETRY_WAITING_TIME`, `MON_INIT_RETRY_COMMON_RATIO` FROM `MAINCONF` WHERE `PK`=1';
        $result = mysql_query($query, $GLOBALS['DB']);

        if (mysql_num_rows($result))
        {
            $row = mysql_fetch_assoc($result);
            $mc->CONF_TITLE = $row['CONF_TITLE'];
            $mc->MAX_MONITOR_THREAD = $row['MAX_MONITOR_THREAD'];
            $mc->MON_LOAD_ITERATION = $row['MON_LOAD_ITERATION'];
            $mc->MON_CHECK_ITERATION = $row['MON_CHECK_ITERATION'];
            $mc->MON_TIMEOUT_LIMIT = $row['MON_TIMEOUT_LIMIT'];
            $mc->MON_INIT_RETRY_WAITING_TIME = $row['MON_INIT_RETRY_WAITING_TIME'];
            $mc->MON_INIT_RETRY_COMMON_RATIO = $row['MON_INIT_RETRY_COMMON_RATIO'];
            $mc->PK = 1;
        }
        mysql_free_result($result);

        return $mc;
    }

    public function save()
    {
        if ($this->PK)
        {
            $query = sprintf('UPDATE `MAINCONF` SET `CONF_TITLE`="%s",`MAX_MONITOR_THREAD`=%d,`MON_LOAD_ITERATION`=%d,`MON_CHECK_ITERATION`=%d,`MON_TIMEOUT_LIMIT`=%d,`MON_INIT_RETRY_WAITING_TIME`=%d,`MON_INIT_RETRY_COMMON_RATIO`=%d WHERE `PK`=1',
                $this->CONF_TITLE,
                $this->MAX_MONITOR_THREAD,
                $this->MON_LOAD_ITERATION,
                $this->MON_CHECK_ITERATION,
                $this->MON_TIMEOUT_LIMIT,
                $this->MON_INIT_RETRY_WAITING_TIME,
                $this->MON_INIT_RETRY_COMMON_RATIO);
            mysql_query($query, $GLOBALS['DB']);
        }
    }
}
?>
