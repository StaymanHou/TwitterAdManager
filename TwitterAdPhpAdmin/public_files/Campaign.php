<?php

include '../lib/common.php';
include '../lib/db.php';
include '../model/Campaign.php';

$method = (isset($_GET['method'])) ? $_GET['method'] : null;

if ($method=='kill')
{
    $fi_id = (isset($_GET['fi_id'])) ? $_GET['fi_id'] : null;
    Campaign::killalive($fi_id);
    header('Location: ' . $_SERVER['HTTP_REFERER']);
}
else
{
   header('HTTP/1.0 403 Forbidden');
}

?>
