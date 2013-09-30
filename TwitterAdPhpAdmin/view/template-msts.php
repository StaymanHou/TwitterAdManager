<div id="MS_MainConf">
 <h2>Main Config</h2>
 <table border=1>
  <tr>
   <td title="The title of the configuration. There's no meaning so far.">Config Title</td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->CONF_TITLE;?></td>
  </tr>
  <tr>
   <td title="If you set a larger value, the program will be more fast, but it will also comsume more system resources. Vice versa.">Max thread number of monitors Title</td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MAX_MONITOR_THREAD;?></td>
  </tr>
  <tr>
   <td title="The minimum iteration between each request to the Twitter server.">Monitor load iteration</td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MON_LOAD_ITERATION;?></td>
  </tr>
  <tr>
   <td>Monitor check iteration</td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MON_CHECK_ITERATION;?></td>
  </tr>
  <tr>
   <td>Monitor timeout limit</td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MON_TIMEOUT_LIMIT;?></td>
  </tr>
  <tr>
   <td>Monitor initial retry waiting time</td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MON_INIT_RETRY_WAITING_TIME;?></td>
  </tr>
  <tr>
   <td>Monitor retry increase common ratio</td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MON_INIT_RETRY_COMMON_RATIO;?></td>
  </tr>
 </table>
 <div class="abuttonwrapper"><a class="abutton" href="MainConf.php?method=get"><span>Modify main config</span></a></div>
</div>
<div id="MS_AccInfo">
 <h2>Accounts Info</h2>
 <table border=1>
  <tr>
   <td>Account Number</td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['ActAccNum'] . ' / ' . $GLOBALS['TEMPLATE']['Content']['TotAccNum'] . ' active/total'?></td>
  </tr>
 </table>
</div>
<div id="MS_Sum">
 <h2>Summary</h2>
 <table border=1>
  <tr>
   <td><div class="abuttonwrapper"><a class="abutton" href="#"><span>Change Period</span></a></div></td>
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
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumPeriodStart'] . ' ~ ' . $GLOBALS['TEMPLATE']['Content']['SumPeriodEnd'];?></td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumPeriod']->imp;?></td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumPeriod']->eng;?></td>
   <td>$<?php echo $GLOBALS['TEMPLATE']['Content']['SumPeriod']->spd;?></td>
  </tr>
  <tr>
   <td>Total</td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumTotal']->imp;?></td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['SumTotal']->eng;?></td>
   <td>$<?php echo $GLOBALS['TEMPLATE']['Content']['SumTotal']->spd;?></td>
  </tr>
 </table>
</div>
<div id="MS_Cmp">
 <h2>Campaign Info</h2>
 <table border=1>
  <tr>
   <td>Total</td>
   <td><?php echo $GLOBALS['TEMPLATE']['Content']['CampaignsTotal'];?></td>
  </tr>
<?php
foreach ($GLOBALS['TEMPLATE']['Content']['Campaigns'] as $key => $value) {
    echo '<tr><td>' . $key . '</td><td>' . $value . '</td></tr>';
}
?>
 </table>
 <div class="abuttonwrapper"><a class="abutton" href="Reset.php?method=normal" style="background: transparent url('media/square-orange-left.gif') no-repeat top left" onclick="return myconfirm('Are you sure you want to reset the campaign database and the summary database?\nThe data to be deleted will be backuped into the mysql folder.');"><span style="background: transparent url('media/square-orange-right.gif') no-repeat top right">Reset Campaign and Summary</span></a></div>
</div>

