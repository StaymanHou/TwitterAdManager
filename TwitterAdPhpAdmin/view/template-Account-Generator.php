<form method="post"
 action="Account.php?method=gensave">
 <table>
  <tr>
   <td width="100px"><label for="USERNAME">Username</label></td>
   <td><input type="text" name="USERNAME" id="USERNAME"
    value="<?php echo $acc->USERNAME;?>" readonly/></td>
  </tr>
  <tr>
   <td><label for="USER">Target User</label></td>
   <td>(lower)<input type="text" name="USER_NUM_LOW" id="USER_NUM_LOW"
    value="<?php echo $acc->USER_NUM_LOW;?>" maxlength="4" size="4"/> ~ <input type="text" name="USER_NUM_HIGH" id="USER_NUM_HIGH"
    value="<?php echo $acc->USER_NUM_HIGH;?>" maxlength="4" size="4"/>(upper) | Private Weight: <input type="text" name="USER_PRIVATE_WEIGHT" id="USER_PRIVATE_WEIGHT"
    value="<?php echo $acc->USER_PRIVATE_WEIGHT;?>" size="5"/></td>
  </tr>
  <tr>
   <td><label for="INTST">Target Interest</label></td>
   <td>(lower)<input type="text" name="INTST_NUM_LOW" id="INTST_NUM_LOW"
    value="<?php echo $acc->INTST_NUM_LOW;?>" maxlength="4" size="4"/> ~ <input type="text" name="INTST_NUM_HIGH" id="INTST_NUM_HIGH"
    value="<?php echo $acc->INTST_NUM_HIGH;?>" maxlength="4" size="4"/>(upper) | Private Weight: <input type="text" name="INTST_PRIVATE_WEIGHT" id="INTST_PRIVATE_WEIGHT"
    value="<?php echo $acc->INTST_PRIVATE_WEIGHT;?>" size="5"/></td>
  </tr>
  <tr>
   <td><label for="CNTRY">Target Country</label></td>
   <td>(lower)<input type="text" name="CNTRY_NUM_LOW" id="CNTRY_NUM_LOW"
    value="<?php echo $acc->CNTRY_NUM_LOW;?>" maxlength="4" size="4"/> ~ <input type="text" name="CNTRY_NUM_HIGH" id="CNTRY_NUM_HIGH"
    value="<?php echo $acc->CNTRY_NUM_HIGH;?>" maxlength="4" size="4"/>(upper) | Private Weight: <input type="text" name="CNTRY_PRIVATE_WEIGHT" id="CNTRY_PRIVATE_WEIGHT"
    value="<?php echo $acc->CNTRY_PRIVATE_WEIGHT;?>" size="5"/></td>
  </tr>
  <tr>
   <td><label for="BID">Bid Price</label></td>
   <td>(lower)<input type="text" name="BID_LOW" id="BID_LOW"
    value="<?php echo $acc->BID_LOW;?>" size="4"/> ~ <input type="text" name="BID_HIGH" id="BID_HIGH"
    value="<?php echo $acc->BID_HIGH;?>" size="4"/>(upper)</td>
  </tr>
  <tr>
   <td><label for="BUDGET">Budget</label></td>
   <td>Campaign: <input type="text" name="CMP_BUDGET" id="CMP_BUDGET"
    value="<?php echo $acc->CMP_BUDGET;?>" size="6"/> | Daily <input type="text" name="DLY_BUDGET" id="DLY_BUDGET"
    value="<?php echo $acc->DLY_BUDGET;?>" size="6"/></td>
  </tr>
  <tr>
   <td><label for="PTS">Pac To Similar</label></td>
   <td>
    <select name="PTS" id="PTS">
     <option value="0" <?php if ($acc->PTS=="0") {echo 'selected="selected"';}?>>False</option>
     <option value="1" <?php if ($acc->PTS=="1") {echo 'selected="selected"';}?>>True</option>
   </select> 
  </tr>
  <tr>
   <td><label for="GENDER">Gender</label></td>
   <td>
    <select name="GENDER" id="GENDER">
<?php
foreach ($gdlst as $key => $value) {
    echo '<option value="' . $key .'" ';
    if ($acc->GENDER==strval($key)) {echo 'selected="selected"';}
    echo '>' . $value . '</option>';
}
?>
   </select> 
  </tr>
  <tr>
   <td><label for="ACCELERATED_DELIVERY">Accelerated Delivery</label></td>
   <td>
    <select name="ACCELERATED_DELIVERY" id="ACCELERATED_DELIVERY">
     <option value="0" <?php if ($acc->ACCELERATED_DELIVERY=="0") {echo 'selected="selected"';}?>>False</option>
     <option value="1" <?php if ($acc->ACCELERATED_DELIVERY=="1") {echo 'selected="selected"';}?>>True</option>
   </select> 
  </tr>
  <tr>
   <td><label for="KILL">Kill current alive campaigns?</label></td>
   <td>
    <input type="radio" name="KILL" value="1" checked>Yes<br>
    <input type="radio" name="KILL" value="0">No<br>
   </td>
  </tr>
  <tr>
   <td> </td>
   <td>
    <input type="submit" style="float: left;" value="Save" onclick="return myconfirm('Are you sure you want to save the changes?\nIf you don\'t kill current alive campaigns, it may be treated equally as the campaigns generated in future?');"/>
    <div class="abuttonwrapper" style="float: right; width: auto;"><a class="abutton" href="accmng.php" onclick="return myconfirm('Are you sure you want to cancel the changes?');"><span>Cancel</span></a></div>
   </td>
   <td><input type="hidden" name="submitted" value="1"/></td>
   <td><input type="hidden" name="PK" value="<?php echo $acc->PK;?>"/></td>
  </tr>
 </table>
</form>

