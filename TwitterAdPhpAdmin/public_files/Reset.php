<?php

include '../lib/common.php';
include '../lib/db.php';
include '../model/Campaign.php';
include '../model/Summary.php';

$method = (isset($_GET['method'])) ? $_GET['method'] : null;

if ($method=='normal')
{
    Campaign::reset();
    Summary::reset();
    header('Location: ' . $_SERVER['HTTP_REFERER']);
}
else
{
   header('HTTP/1.0 403 Forbidden');
}

?>
