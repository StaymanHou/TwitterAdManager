<form method="post"
 action="Account.php?method=basicsave">
 <table>
  <tr>
   <td><label for="USERNAME">Username</label></td>
   <td><input type="text" name="USERNAME" id="USERNAME"
    value="<?php echo $acc->USERNAME;?>"/></td>
  </tr>
  <tr>
   <td><label for="PSWD">Password</label></td>
   <td><input type="password" name="PSWD" id="PSWD"
    value="<?php echo $acc->PSWD;?>"/></td>
  </tr>
  <tr>
   <td><label for="FI_ID">fi_id</label></td>
   <td><input type="text" name="FI_ID" id="FI_ID"
    value="<?php echo $acc->FI_ID;?>" <?php if ($acc->FI_ID!=null) { echo 'readonly';}?>/></td>
  </tr>
  <tr>
   <td><label for="ACTIVE">Active</label></td>
   <td>
    <select name="ACTIVE" id="ACTIVE">
     <option value="0" <?php if ($acc->ACTIVE=="0") {echo 'selected="selected"';}?>>False</option>
     <option value="1" <?php if ($acc->ACTIVE=="1") {echo 'selected="selected"';}?>>True</option>
   </select> 
  </tr>
  <tr>
   <td><label for="BUDGET_LIMIT_THRESHOLD">Budget Low Threshold</label></td>
   <td><input type="text" name="BUDGET_LIMIT_THRESHOLD" id="BUDGET_LIMIT_THRESHOLD"
    value="<?php echo $acc->BUDGET_LIMIT_THRESHOLD;?>"/></td>
  </tr>
  <tr>
   <td><label for="POOR_ZSCORE_THRESHOLD">Poor Zscore Threshold</label></td>
   <td><input type="text" name="POOR_ZSCORE_THRESHOLD" id="POOR_ZSCORE_THRESHOLD"
    value="<?php echo $acc->POOR_ZSCORE_THRESHOLD;?>"/></td>
  </tr>
  <tr>
   <td><label for="EFFECTIVE_DAYS">Analyze Effective Days</label></td>
   <td><input type="text" name="EFFECTIVE_DAYS" id="EFFECTIVE_DAYS"
    value="<?php echo $acc->EFFECTIVE_DAYS;?>"/></td>
  </tr>
  <tr>
   <td><label for="MAX_CAMPAIGN_NUM">Max Campaign Number</label></td>
   <td><input type="text" name="MAX_CAMPAIGN_NUM" id="MAX_CAMPAIGN_NUM"
    value="<?php echo $acc->MAX_CAMPAIGN_NUM;?>"/></td>
  </tr>
  </tr>
   <td> </td>
   <td>
    <input type="submit" style="float: left;" value="Save" onclick="return myconfirm('Are you sure you want to save it?');"/>
    <div class="abuttonwrapper" style="float: right; width: auto;"><a class="abutton" href="accmng.php" onclick="return myconfirm('Are you sure you want to cancel it?');"><span>Cancel</span></a></div>
   </td>
   <td><input type="hidden" name="submitted" value="1"/></td>
   <td><input type="hidden" name="PK" value="<?php echo $acc->PK;?>"/></td>
  </tr>
 </table>
</form>

