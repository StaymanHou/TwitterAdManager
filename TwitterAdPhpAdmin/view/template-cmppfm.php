<script>
var imp_week_data = <?php echo json_encode($imp_week_data); ?>;
var eng_week_data = <?php echo json_encode($eng_week_data); ?>;
var week_label = <?php echo json_encode($week_label); ?>;
var imp_day_data = <?php echo json_encode($imp_day_data); ?>;
var eng_day_data = <?php echo json_encode($eng_day_data); ?>;
var day_label = <?php echo json_encode($day_label); ?>;
</script>

<div id="CP_Menu">
 <table border=1>
 <tr><td><div<?php if ($GLOBALS['TEMPLATE']['Content']['curfiid']==null) {echo ' class="curnavitem"';}?>><a href="cmppfm.php">All</a></div></td></tr>
<?php
$accFtU = array();
foreach ($GLOBALS['TEMPLATE']['Content']['AccList'] as $acc)
{
    echo '<tr><td><div';
    if ($GLOBALS['TEMPLATE']['Content']['curfiid']==$acc['FI_ID']) {echo ' class="curnavitem"';};
    echo '><a href="cmppfm.php?fi_id=';
    echo $acc['FI_ID'];
    echo '">' . $acc['USERNAME'] . '</a></div></tr></td>';
    $accFtU[$acc['FI_ID']]=$acc['USERNAME'];
}
?>
 </table>
</div>
<div id="CP_Wrapper">
 <div id="CP_Summary">
  <h2>Summary</h2>
  <table border=1>
   <tr>
    <td><div class="abuttonwrapper"><a class="abutton" href="cmppfm_summary.php"><span>Download .csv</span></a></div></td>
    <td>Impression</td><td>Engagement</td><td>Spend</td>
   </tr>
   <tr>
    <td>Today</td>
    <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumToday']->imp;?></td>
    <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumToday']->eng;?></td>
    <td>$<?php echo $GLOBALS['TEMPLATE']['Content']['SumToday']->spd;?></td>
   </tr>
   <tr>
    <td>Yesterday</td>
    <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumYester']->imp;?></td>
    <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumYester']->eng;?></td>
    <td>$<?php echo $GLOBALS['TEMPLATE']['Content']['SumYester']->spd;?></td>
   </tr>
   <tr>
    <td>Last 7 Days</td>
    <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumSevenDays']->imp;?></td>
    <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumSevenDays']->eng;?></td>
    <td>$<?php echo $GLOBALS['TEMPLATE']['Content']['SumSevenDays']->spd;?></td>
   </tr>
   <tr>
    <td>Total</td>
    <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumTotal']->imp;?></td>
    <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumTotal']->eng;?></td>
    <td>$<?php echo $GLOBALS['TEMPLATE']['Content']['SumTotal']->spd;?></td>
   </tr>
  </table>
 </div>
 <div id="CP_Chart">
  <h2>Chart</h2>
  <div id="weekchart"></div>
  <script>myweekchart(imp_week_data,eng_week_data,week_label);</script>
  <div id="daychart"></div>
  <script>mydaychart(imp_day_data,eng_day_data,day_label);</script>
 </div>
</div>
<div id="CP_Detail">
 <h2>Campaign Detail</h2>
 <div id="CP_Detail_Nav">
  <div class="<?php if ($GLOBALS['TEMPLATE']['Content']['curls']==null) {echo 'cur';} ?>cpnavitem"><a href="cmppfm.php?fi_id=<?php if ($GLOBALS['TEMPLATE']['Content']['curfiid']!=null) {echo $GLOBALS['TEMPLATE']['Content']['curfiid'];}?>">Total <?php echo '[' . $GLOBALS['TEMPLATE']['Content']['CampaignsTotal'] . ']';?></a></div>
<?php
foreach ($GLOBALS['TEMPLATE']['Content']['Campaigns'] as $key => $value) {
    echo '<div class="';
    if ($GLOBALS['TEMPLATE']['Content']['curls']==$lslst[$key]) {echo 'cur';}
    echo 'cpnavitem"><a href="cmppfm.php?fi_id=';
    if ($GLOBALS['TEMPLATE']['Content']['curfiid']!=null) {echo $GLOBALS['TEMPLATE']['Content']['curfiid'];}
    echo '&local_status=';
    echo $lslst[$key];
    echo '">';
    echo $key . ' ';
    echo '[' . $value . ']';
    echo '</a></div>';
}
?>
  <div class="abuttonwrapper cpnavitem"><a class="abutton" href="Campaign.php?method=kill&fi_id=<?php if ($GLOBALS['TEMPLATE']['Content']['curfiid']!=null) {echo $GLOBALS['TEMPLATE']['Content']['curfiid'];}?>" style="background: transparent url('media/square-orange-left.gif') no-repeat top left" onclick="return myconfirm('Are you sure you want to put every Alive and CreatePending Campaigns of \'<?php echo $GLOBALS['TEMPLATE']['Content']['curfiid']?$accFtU[$GLOBALS['TEMPLATE']['Content']['curfiid']]:'All';?>\' into DeletePending?');"><span style="background: transparent url('media/square-orange-right.gif') no-repeat top right">Kill all alive & createpending campaigns</span></a></div>
 </div>
 <div id="CP_Detail_List">
  <table border=1>
   <tr>
    <td>Campaign Name</td>
    <td>Status</td>
    <td>Acitve</td>
    <td>Start Time</td>
    <td>End Time</td>
    <td>Account</td>
    <td>Total Budget</td>
    <td>Daily Budget</td>
    <td>Max Bid</td>
    <td>Targeted User Number</td>
    <td>Targeted Interest Number</td>
    <td>Location Number</td>
    <td>PTS</td>
    <td>Gender</td>
    <td>AD mode</td>
   </tr>
<?php
foreach ($GLOBALS['TEMPLATE']['Content']['CampaignsList'] as $cmp) {
    echo '<tr><td>' . $cmp['NAME'] . '</td><td>' . $lsptt[$cmp['LOCAL_STATUS']] . '</td><td>';
    echo $cmp['ACTIVE']?'True':'False';
    echo '</td><td>' . $cmp['START_TIME'] . '</td><td>' . $cmp['END_TIME'] . '</td><td>' . $accptt[$cmp['FI_ID']] . '</td><td>$' . $cmp['TOTAL_BUDGET'] . '</td><td>$' . $cmp['DAILY_BUDGET'] . '</td><td>$' . $cmp['MAX_BID'] . '</td><td>';
    echo $cmp['TARGETED_USERS']==''?'0':strval(1+substr_count($cmp['TARGETED_USERS'], ','));
    echo '</td><td>';
    echo $cmp['TARGETED_INTERESTS']==''?'0':strval(1+substr_count($cmp['TARGETED_INTERESTS'], ','));
    echo '</td><td>';
    echo $cmp['LOCATIONS']==''?'0':strval(1+substr_count($cmp['LOCATIONS'], ','));
    echo '</td><td>';
    echo $cmp['PAC_TO_SIMILAR']?'True':'False';
    echo '</td><td>' . $gdptt[$cmp['GENDER']] . '</td><td>';
    echo $cmp['ACCELERATED_DELIVERY']?'True':'False';
    echo '</td></tr>';
}
?>
  </table>
 </div>
</div>
