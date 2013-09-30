<form method="post"
 action="MainConf.php?method=save">
 <table>
  <tr>
   <td title="The title of the configuration. There's no meaning so far."><label for="CONF_TITLE">Config Title</label></td>
   <td><input type="text" name="CONF_TITLE" id="CONF_TITLE"
    value="<?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->CONF_TITLE;?>"/></td>
  </tr>
  <tr>
   <td title="If you set a larger value, the program will be more fast, but it will also comsume more system resources. Vice versa."><label for="MAX_MONITOR_THREAD">Max thread number of monitors Title</label></td>
   <td><input type="text" name="MAX_MONITOR_THREAD" id="MAX_MONITOR_THREAD"
    value="<?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MAX_MONITOR_THREAD;?>"/></td>
  </tr>
  <tr>
   <td title="The minimum iteration between each request to the Twitter server."><label for="MON_LOAD_ITERATION">Monitor load iteration</label></td>
   <td><input type="text" name="MON_LOAD_ITERATION" id="MON_LOAD_ITERATION"
    value="<?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MON_LOAD_ITERATION;?>"/></td>
  </tr>
  <tr>
   <td><label for="MON_CHECK_ITERATION">Monitor check iteration</label></td>
   <td><input type="text" name="MON_CHECK_ITERATION" id="MON_CHECK_ITERATION"
    value="<?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MON_CHECK_ITERATION;?>"/></td>
  </tr>
  <tr>
   <td><label for="MON_TIMEOUT_LIMIT">Monitor timeout limit</label></td>
   <td><input type="text" name="MON_TIMEOUT_LIMIT" id="MON_TIMEOUT_LIMIT"
    value="<?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MON_TIMEOUT_LIMIT;?>"/></td>
  </tr>
  <tr>
   <td><label for="MON_INIT_RETRY_WAITING_TIME">Monitor initial retry waiting time</label></td>
   <td><input type="text" name="MON_INIT_RETRY_WAITING_TIME" id="MON_INIT_RETRY_WAITING_TIME"
    value="<?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MON_INIT_RETRY_WAITING_TIME;?>"/></td>
  </tr>
  <tr>
   <td><label for="MON_INIT_RETRY_COMMON_RATIO">Monitor retry increase common ratio</label></td>
   <td><input type="text" name="MON_INIT_RETRY_COMMON_RATIO" id="MON_INIT_RETRY_COMMON_RATIO"
    value="<?php echo $GLOBALS['TEMPLATE']['Content']['MainConf']->MON_INIT_RETRY_COMMON_RATIO;?>"/></td>
  </tr>
   <td> </td>
   <td>
    <input type="submit" style="float: left;" value="Save" onclick="return myconfirm('Are you sure you want to save the changes?');"/>
    <div class="abuttonwrapper" style="float: right; width: auto;"><a class="abutton" href="mainstatus.php" onclick="return myconfirm('Are you sure you want to cancel the changes?');"><span>Cancel</span></a></div>
   </td>
   <td><input type="hidden" name="submitted" value="1"/></td>
  </tr>
 </table>
</form>

