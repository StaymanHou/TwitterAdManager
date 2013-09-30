<?php

include '../lib/common.php';
include '../lib/db.php';
include '../model/MainConf.php';
include '../model/Account.php';
include '../model/Summary.php';
include '../model/Campaign.php';
include '../model/LocalStatus.php';

$timezone = new DateTimeZone(date_default_timezone_get());
$offset = $timezone->getOffset(new DateTime("now"));

$GLOBALS['TEMPLATE']['title'] = 'Main Status';
$GLOBALS['TEMPLATE']['curnav'] = 'MainStatus';
$GLOBALS['TEMPLATE']['ContentViewFile'] = 'template-msts.php';

$period_start = (isset($_GET['period_start'])) ? intval($_GET['period_start']) : intval((time()+$offset)/86400)*86400-86400*6-$offset;
$period_end = (isset($_GET['period_end'])) ? intval($_GET['period_end']) : intval((time()-3600)/3600)*3600;

$GLOBALS['TEMPLATE']['Content']['MainConf'] = MainConf::get();

$GLOBALS['TEMPLATE']['Content']['ActAccNum'] = Account::getactivenum();
$GLOBALS['TEMPLATE']['Content']['TotAccNum'] = Account::gettotalnum();

$lastHour = intval((time()-3600)/3600)*3600;
$zeroToday = intval((time()+$offset)/86400)*86400-$offset;
$zeroYester = intval((time()+$offset)/86400)*86400-86400-$offset;

$GLOBALS['TEMPLATE']['Content']['SumToday'] = Summary::gettotal($zeroToday, $lastHour);
$GLOBALS['TEMPLATE']['Content']['SumYester'] = Summary::gettotal($zeroYester, $zeroToday);
$GLOBALS['TEMPLATE']['Content']['SumPeriod'] = Summary::gettotal($period_start, $period_end);
$GLOBALS['TEMPLATE']['Content']['SumPeriodStart'] = date("m-d:H", $period_start);
$GLOBALS['TEMPLATE']['Content']['SumPeriodEnd'] = date("m-d:H", $period_end);
$GLOBALS['TEMPLATE']['Content']['SumTotal'] = Summary::gettotal();

$lslst = LocalStatus::getTtPDict();
foreach ($lslst as $key => $value) {
    $GLOBALS['TEMPLATE']['Content']['Campaigns'][$key] = Campaign::getnum(null, $value);
}
$GLOBALS['TEMPLATE']['Content']['CampaignsTotal'] = Campaign::getnum();

//var_dump($GLOBALS['TEMPLATE']['Content']['MainConf']->CONF_TITLE);

include '../view/template-page.php';
?>
