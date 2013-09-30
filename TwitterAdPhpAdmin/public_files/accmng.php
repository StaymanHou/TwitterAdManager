<?php

include '../lib/common.php';
include '../lib/db.php';
include '../model/Account.php';
include '../model/LocalStatus.php';

$GLOBALS['TEMPLATE']['title'] = 'Account Management';
$GLOBALS['TEMPLATE']['curnav'] = 'AccMng';
$GLOBALS['TEMPLATE']['ContentViewFile'] = 'template-accmng.php';

$GLOBALS['TEMPLATE']['Content']['ActAccNum'] = Account::getactivenum();
$GLOBALS['TEMPLATE']['Content']['TotAccNum'] = Account::gettotalnum();

$GLOBALS['TEMPLATE']['Content']['AccList'] = Account::getlist();

//var_dump($GLOBALS['TEMPLATE']['Content']);

include '../view/template-page.php';
?>
