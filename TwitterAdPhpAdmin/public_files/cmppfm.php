<?php

include '../lib/common.php';
include '../lib/db.php';
include '../model/Account.php';
include '../model/Summary.php';
include '../model/Campaign.php';
include '../model/LocalStatus.php';
include '../model/Gender.php';

$timezone = new DateTimeZone(date_default_timezone_get());
$offset = $timezone->getOffset(new DateTime("now"));

$GLOBALS['TEMPLATE']['jsheader'] = '<script src="../public_files/js/d3.v3.js" charset="utf-8"></script><script src="../public_files/js/mychart.js" charset="utf-8"></script>';
$GLOBALS['TEMPLATE']['title'] = 'Campaign Performance';
$GLOBALS['TEMPLATE']['curnav'] = 'CmpPfm';
$GLOBALS['TEMPLATE']['ContentViewFile'] = 'template-cmppfm.php';

$GLOBALS['TEMPLATE']['Content']['curfiid'] = (isset($_GET['fi_id'])) ? $_GET['fi_id'] : null;
$GLOBALS['TEMPLATE']['Content']['curls'] = (isset($_GET['local_status'])) ? $_GET['local_status'] : null;

$GLOBALS['TEMPLATE']['Content']['AccList'] = Account::getlist();

$lastHour = intval((time()-3600)/3600)*3600;
$zeroToday = intval((time()+$offset)/86400)*86400-$offset;
$zeroYester = intval((time()+$offset)/86400)*86400-86400-$offset;
$zeroSevenDays = intval((time()+$offset)/86400)*86400-86400*6-$offset;

$GLOBALS['TEMPLATE']['Content']['SumToday'] = Summary::gettotal($zeroToday, $lastHour, $GLOBALS['TEMPLATE']['Content']['curfiid']);
$GLOBALS['TEMPLATE']['Content']['SumYester'] = Summary::gettotal($zeroYester, $zeroToday, $GLOBALS['TEMPLATE']['Content']['curfiid']);
$GLOBALS['TEMPLATE']['Content']['SumSevenDays'] = Summary::gettotal($zeroSevenDays, $lastHour, $GLOBALS['TEMPLATE']['Content']['curfiid']);
$GLOBALS['TEMPLATE']['Content']['SumTotal'] = Summary::gettotal(null,null,$GLOBALS['TEMPLATE']['Content']['curfiid']);

$week_ago_epoch = mktime(0, 0, 0, date("m")  , date("d")-7, date("Y"));
$tfhour_ago_epoch = mktime(date("H"), date("i"), date("s"), date("m")  , date("d")-1, date("Y"));
$now_epoch = mktime(date("H"), date("i"), date("s"), date("m")  , date("d"), date("Y"));

$imp_week_data = array_fill(0,8,0);
$eng_week_data = array_fill(0,8,0);
$week_label = array_fill(0,8,"");
$imp_day_data = array_fill(0,25,0);
$eng_day_data = array_fill(0,25,0);
$day_label = array_fill(0,25,"");

$result = Summary::getlist($week_ago_epoch, $now_epoch, $GLOBALS['TEMPLATE']['Content']['curfiid']);

while ($row = mysql_fetch_array($result))
{
    $row['PERIOD_END'] = strtotime($row['PERIOD_END']);
    $row['NEW_IMPRESSIONS'] = intval($row['NEW_IMPRESSIONS']);
    $row['NEW_ENGAGEMENTS'] = intval($row['NEW_ENGAGEMENTS']);
    if(isset($row)){
    $imp_week_data[floor(($row['PERIOD_END']-$week_ago_epoch-3600)/86400)] += $row['NEW_IMPRESSIONS'];
    $eng_week_data[floor(($row['PERIOD_END']-$week_ago_epoch-3600)/86400)] += $row['NEW_ENGAGEMENTS'];
        if(intval($row['PERIOD_END'])>=intval($tfhour_ago_epoch)&&intval($row['PERIOD_END'])<intval($tfhour_ago_epoch)+3600*25){
            $imp_day_data[floor(($row['PERIOD_END']-$tfhour_ago_epoch)/3600)] += $row['NEW_IMPRESSIONS'];
            $eng_day_data[floor(($row['PERIOD_END']-$tfhour_ago_epoch)/3600)] += $row['NEW_ENGAGEMENTS'];
        }
    }
}

for ($i=0;$i<8;$i++){
    $epoch = $week_ago_epoch+3600+$i*86400;
    $week_label[$i] = date('m-d', $epoch);
}

for ($i=0;$i<25;$i++){
    $epoch = $tfhour_ago_epoch+$i*3600;
    $day_label[$i] = date('[d]H', $epoch); // convert UNIX timestamp to PHP DateTime
}

$lslst = LocalStatus::getTtPDict();
foreach ($lslst as $key => $value) {
    $GLOBALS['TEMPLATE']['Content']['Campaigns'][$key] = Campaign::getnum($GLOBALS['TEMPLATE']['Content']['curfiid'], $value);
}
$GLOBALS['TEMPLATE']['Content']['CampaignsTotal'] = Campaign::getnum( $GLOBALS['TEMPLATE']['Content']['curfiid'], $GLOBALS['TEMPLATE']['Content']['curls']);

$accptt = array();
foreach ($GLOBALS['TEMPLATE']['Content']['AccList'] as $acc) {
    $accptt[$acc['FI_ID']] = $acc['USERNAME'];
}
$lsptt = LocalStatus::getPtTDict();
$gdptt = Gender::getPtTDict();
$GLOBALS['TEMPLATE']['Content']['CampaignsList'] = Campaign::getlist( $GLOBALS['TEMPLATE']['Content']['curfiid'], $GLOBALS['TEMPLATE']['Content']['curls']);

include '../view/template-page.php';
?>
