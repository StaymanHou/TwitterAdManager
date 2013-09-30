<?php
class Gender
{
    // return an object populated based on the record's user id
    public static function getPtTDict()
    {
        $dict = array();

        $query = 'SELECT * FROM Genders';
        $result = mysql_query($query, $GLOBALS['DB']);
        while ($row = mysql_fetch_assoc($result)) {
            $dict[$row['PK']] = $row['TITLE'];
        }
        mysql_free_result($result);

        return $dict;
    }

    // return an object populated based on the record's user id
    public static function getTtPDict()
    {
        $dict = array();

        $query = 'SELECT * FROM Genders';
        $result = mysql_query($query, $GLOBALS['DB']);
        while ($row = mysql_fetch_assoc($result)) {
            $dict[$row['TITLE']] = $row['PK'];
        }
        mysql_free_result($result);

        return $dict;
    }
}
?>
