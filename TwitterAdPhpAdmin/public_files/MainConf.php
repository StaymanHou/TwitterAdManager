<?php

include '../lib/common.php';
include '../lib/db.php';
include '../model/MainConf.php';

$method = (isset($_GET['method'])) ? $_GET['method'] : null;

if ($method=='get')
{
    $GLOBALS['TEMPLATE']['title'] = 'Modify Main Config';
    $GLOBALS['TEMPLATE']['ContentViewFile'] = 'template-MainConf.php';

    $GLOBALS['TEMPLATE']['Content']['MainConf'] = MainConf::get();

    include '../view/template-page.php';
}
else if ($method=='save'&&isset($_POST['submitted']))
{
    $mc = MainConf::get();
    $mc->CONF_TITLE = $_POST['CONF_TITLE'];
    $mc->MAX_MONITOR_THREAD = $_POST['MAX_MONITOR_THREAD'];
    $mc->MON_LOAD_ITERATION = $_POST['MON_LOAD_ITERATION'];
    $mc->MON_CHECK_ITERATION = $_POST['MON_CHECK_ITERATION'];
    $mc->MON_TIMEOUT_LIMIT = $_POST['MON_TIMEOUT_LIMIT'];
    $mc->MON_INIT_RETRY_WAITING_TIME = $_POST['MON_INIT_RETRY_WAITING_TIME'];
    $mc->MON_INIT_RETRY_COMMON_RATIO = $_POST['MON_INIT_RETRY_COMMON_RATIO'];
    $mc->save();
    header('Location: mainstatus.php');
}
else
{
   header('HTTP/1.0 403 Forbidden');
}

?>
