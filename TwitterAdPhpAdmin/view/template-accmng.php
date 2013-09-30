<div id="AM_Summary">
 <h2>Summary</h2>
 <table border=1>
  <tr>
   <td>Account Number</td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['ActAccNum'] . ' / ' . $GLOBALS['TEMPLATE']['Content']['TotAccNum'] . ' active/total'?></td>
  </tr>
 </table>
</div>
<div id="AM_List">
 <h2>Detialed List</h2>
 <div class="abuttonwrapper"><a class="abutton" href="Account.php?method=create"><span>Create new account</span></a></div>
 <table border=1>
 <tr>
  <td>FI_ID</td>
  <td>Username</td>
  <td>Active</td>
  <td>Account budget</td>
  <td style="color: GoldenRod;">Budget remain</td>
  <td width="76px">Change budget</td>
  <td width="65px">Budget low threshold</td>
  <td width="55px">Zscore threshold</td>
  <td width="50px">Effective days</td>
  <td>Max campaign number</td>
  <td>Bid lower bound</td>
  <td>Bid upper bound</td>
  <td width="66px">Deactive /Active</td>
  <td width="89px">Modify</td>
  <td>Delete</td>
 </tr>
<?php
foreach ($GLOBALS['TEMPLATE']['Content']['AccList'] as $acc)
{
    echo '<tr><td>' . $acc['FI_ID'] . '</td>';
    echo '<td>' . $acc['USERNAME'] . '</td>';
    echo '<td style="color: ';
    echo $acc['ACTIVE'] == '0'?'red':'green';
    echo '">';
    echo $acc['ACTIVE'] == '0'?'False':'True';
    echo '</td>';
    echo '<td>$' . $acc['ACC_BUDGET'] . '</td>';
    echo '<td';
    echo floatval($acc['ACC_BUDGET_REMAIN'])<floatval($acc['BUDGET_LIMIT_THRESHOLD'])?' class="lowbudgetremain"':'';
    echo '>$' . $acc['ACC_BUDGET_REMAIN'] . '</td>';
    echo '<td>' . '<div class="abuttonwrapper" style="float:left; width:auto;"><a class="abutton" href="Account.php?method=setbudget&pk=' . $acc['PK'] . '" onclick="return myinput(this,\'set\');"><span>Set</span></a></div>' . '<div class="abuttonwrapper" style="float:left; width:auto;"><a class="abutton" href="Account.php?method=addbudget&pk=' . $acc['PK'] . '" onclick="return myinput(this,\'add\');"><span>Add</span></a></div>' . '</td>';
    echo '<td>$' . $acc['BUDGET_LIMIT_THRESHOLD'] . '</td>';
    echo '<td>' . $acc['POOR_ZSCORE_THRESHOLD'] . '</td>';
    echo '<td>' . $acc['EFFECTIVE_DAYS'] . '</td>';
    echo '<td>' . $acc['MAX_CAMPAIGN_NUM'] . '</td>';
    echo '<td>' . $acc['BID_LOW'] . '</td>';
    echo '<td>' . $acc['BID_HIGH'] . '</td>';
    echo '<td>' . '<div class="abuttonwrapper"><a class="abutton" href="Account.php?method=toggleactive&pk=' . $acc['PK'] . '" style="background: transparent url(\'media/square-';
    echo $acc['ACTIVE'] == '0'?'green':'red';
    echo '-left.gif\') no-repeat top left"><span style="background: transparent url(\'media/square-';
    echo $acc['ACTIVE'] == '0'?'green':'red';
    echo '-right.gif\') no-repeat top right">';
    echo $acc['ACTIVE'] == '0'?'Active':'Deactive';
    echo '</span></a></div>' . '</td>';
    echo '<td>' . '<div class="abuttonwrapper" style="float:left; width:auto;"><a class="abutton" href="Account.php?method=basicget&pk=' . $acc['PK'] . '"><span>Basic</span></a></div>' . '<div class="abuttonwrapper" style="float:left; width:auto;"><a class="abutton" href="Account.php?method=genget&pk=' . $acc['PK'] . '"><span>Gen</span></a></div>' . '</td>';
    echo '<td>' . '<div class="abuttonwrapper"><a class="abutton" href="Account.php?method=delete&pk=' . $acc['PK'] . '" style="background: transparent url(\'media/square-orange-left.gif\') no-repeat top left" onclick="return myconfirm(\'Are you sure you want to delete the account \\\'' . $acc['USERNAME'] . '\\\'?\\n If you delete it, you will no longer be able to create account with the same fi_id.\');"><span style="background: transparent url(\'media/square-orange-right.gif\') no-repeat top right">Delete</span></a></div>' . '</td>';
}
?>
 </table>
</div>
