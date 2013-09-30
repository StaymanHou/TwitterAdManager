<?php

include '../lib/common.php';
include '../lib/db.php';
include '../model/Account.php';
include '../model/Summary.php';

header("Content-type: text/csv");
header("Content-Disposition: attachment; filename=TwitterAdSummary_".time().".csv");
header("Pragma: no-cache");
header("Expires: 0");

$timezone = new DateTimeZone(date_default_timezone_get());
$offset = $timezone->getOffset(new DateTime("now"));

$AccList = Account::getlist();
array_unshift($AccList,array('USERNAME'=>'All','FI_ID'=>null));

$lastHour = intval((time()-3600)/3600)*3600;
$zeroToday = intval((time()+$offset)/86400)*86400-$offset;
$zeroYester = intval((time()+$offset)/86400)*86400-86400-$offset;
$zeroSevenDays = intval((time()+$offset)/86400)*86400-86400*6-$offset;

echo "Account,TodayIMP,TodayENG,TodaySPD,YesterdayIMP,YesterdayENG,YesterdaySPD,Last7DaysIMP,Last7DaysENG,Last7DaysSPD,TotalIMP,TotalENG,TotalSPD\n";

foreach ($AccList as $acc)
{
    echo $acc['USERNAME'];
    $SumToday = Summary::gettotal($zeroToday, $lastHour, $acc['FI_ID']);
    $SumYester = Summary::gettotal($zeroYester, $zeroToday, $acc['FI_ID']);
    $SumSevenDays = Summary::gettotal($zeroSevenDays, $lastHour, $acc['FI_ID']);
    $SumTotal = Summary::gettotal(null,null,$acc['FI_ID']);
    echo ',' . $SumToday->imp . ',' . $SumToday->eng .',' . $SumToday->spd . ',' . $SumYester->imp . ',' . $SumYester->eng .',' . $SumYester->spd . ',' . $SumSevenDays->imp . ',' . $SumSevenDays->eng .',' . $SumSevenDays->spd . ',' . $SumTotal->imp . ',' . $SumTotal->eng .',' . $SumTotal->spd . "\n";
}

?>
