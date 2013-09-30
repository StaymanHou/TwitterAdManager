<?php

include '../lib/common.php';
include '../lib/db.php';
include '../model/Account.php';
include '../model/Gender.php';
include '../model/Campaign.php';

$method = (isset($_GET['method'])) ? $_GET['method'] : null;

if ($method=='toggleactive'&&isset($_GET['pk']))
{
    Account::toggleactive($_GET['pk']);
    header('Location: ' . $_SERVER['HTTP_REFERER']);
}
else if ($method=='delete'&&isset($_GET['pk']))
{
    Account::setdelete($_GET['pk']);
    header('Location: ' . $_SERVER['HTTP_REFERER']);
}
else if ($method=='create')
{
    $GLOBALS['TEMPLATE']['title'] = 'Create New Account';
    $GLOBALS['TEMPLATE']['ContentViewFile'] = 'template-Account-Basic.php';

    $acc = new Account();

    include '../view/template-page.php';
}
else if ($method=='basicget'&&isset($_GET['pk']))
{
    $GLOBALS['TEMPLATE']['title'] = 'Modify Account Basic Setting';
    $GLOBALS['TEMPLATE']['ContentViewFile'] = 'template-Account-Basic.php';

    $acc = Account::getByPK($_GET['pk']);
    $acc->PSWD = '1234567890';

    include '../view/template-page.php';
}
else if ($method=='basicsave'&&isset($_POST['submitted']))
{
    if($_POST['PK']==null)
    {
        $acc = new Account();
        $acc->USERNAME = $_POST['USERNAME'];
        $acc->PSWD = $_POST['PSWD'];
        $acc->FI_ID = $_POST['FI_ID'];
        $acc->ACTIVE = $_POST['ACTIVE'];
        $acc->BUDGET_LIMIT_THRESHOLD = $_POST['BUDGET_LIMIT_THRESHOLD'];
        $acc->POOR_ZSCORE_THRESHOLD = $_POST['POOR_ZSCORE_THRESHOLD'];
        $acc->EFFECTIVE_DAYS = $_POST['EFFECTIVE_DAYS'];
        $acc->MAX_CAMPAIGN_NUM = $_POST['MAX_CAMPAIGN_NUM'];
        $acc->save();
        header('Location: Account.php?method=genget&pk=' . strval($acc->PK));
    } else {
        $acc = Account::getByPK($_POST['PK']);
        if($_POST['PSWD']=='1234567890')
        {
            $acc->USERNAME = $_POST['USERNAME'];
            $acc->ACTIVE = $_POST['ACTIVE'];
            $acc->BUDGET_LIMIT_THRESHOLD = $_POST['BUDGET_LIMIT_THRESHOLD'];
            $acc->POOR_ZSCORE_THRESHOLD = $_POST['POOR_ZSCORE_THRESHOLD'];
            $acc->EFFECTIVE_DAYS = $_POST['EFFECTIVE_DAYS'];
            $acc->MAX_CAMPAIGN_NUM = $_POST['MAX_CAMPAIGN_NUM'];
            $acc->save(false);
        } else {
            $acc->USERNAME = $_POST['USERNAME'];
            $acc->PSWD = $_POST['PSWD'];
            $acc->ACTIVE = $_POST['ACTIVE'];
            $acc->BUDGET_LIMIT_THRESHOLD = $_POST['BUDGET_LIMIT_THRESHOLD'];
            $acc->POOR_ZSCORE_THRESHOLD = $_POST['POOR_ZSCORE_THRESHOLD'];
            $acc->EFFECTIVE_DAYS = $_POST['EFFECTIVE_DAYS'];
            $acc->MAX_CAMPAIGN_NUM = $_POST['MAX_CAMPAIGN_NUM'];
            $acc->save(true);
        }
        header('Location: accmng.php');
    }
}
else if ($method=='genget'&&isset($_GET['pk']))
{
    $GLOBALS['TEMPLATE']['title'] = 'Modify Account Generator Setting';
    $GLOBALS['TEMPLATE']['ContentViewFile'] = 'template-Account-Generator.php';

    $acc = Account::getByPK($_GET['pk']);
    $gdlst = Gender::getPtTDict();

    include '../view/template-page.php';
}
else if ($method=='gensave'&&isset($_POST['submitted']))
{
    $acc = Account::getByPK($_POST['PK']);
    $acc->USER_NUM_LOW = $_POST['USER_NUM_LOW'];
    $acc->USER_NUM_HIGH = $_POST['USER_NUM_HIGH'];
    $acc->USER_PRIVATE_WEIGHT = $_POST['USER_PRIVATE_WEIGHT'];
    $acc->INTST_NUM_LOW = $_POST['INTST_NUM_LOW'];
    $acc->INTST_NUM_HIGH = $_POST['INTST_NUM_HIGH'];
    $acc->INTST_PRIVATE_WEIGHT = $_POST['INTST_PRIVATE_WEIGHT'];
    $acc->CNTRY_NUM_LOW = $_POST['CNTRY_NUM_LOW'];
    $acc->CNTRY_NUM_HIGH = $_POST['CNTRY_NUM_HIGH'];
    $acc->CNTRY_PRIVATE_WEIGHT = $_POST['CNTRY_PRIVATE_WEIGHT'];
    $acc->BID_LOW = $_POST['BID_LOW'];
    $acc->BID_HIGH = $_POST['BID_HIGH'];
    $acc->CMP_BUDGET = $_POST['CMP_BUDGET'];
    $acc->DLY_BUDGET = $_POST['DLY_BUDGET'];
    $acc->PTS = $_POST['PTS'];
    $acc->GENDER = $_POST['GENDER'];
    $acc->ACCELERATED_DELIVERY = $_POST['ACCELERATED_DELIVERY'];
    $acc->save(false,true);
    if ($_POST['KILL']=='1')
    {
        Campaign::killalive($acc->FI_ID);
    }
    header('Location: accmng.php');
}
else if ($method=='setbudget'&&isset($_GET['budget'])&&isset($_GET['pk']))
{
    Account::setbudget($_GET['budget'], $_GET['pk']);
    header('Location: accmng.php');
}
else if ($method=='addbudget'&&isset($_GET['budget'])&&isset($_GET['pk']))
{
    Account::addbudget($_GET['budget'], $_GET['pk']);
    header('Location: accmng.php');
}
else
{
   header('HTTP/1.0 403 Forbidden');
}

?>
