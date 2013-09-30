function myconfirm(my_string)
{
    var agree = confirm(my_string);
    if(agree){return true;}
    else{return false;}
}

function myinput(elem,my_string)
{
    var input=prompt("Please enter the amount you want to "+my_string+".","");
    if (input!=null && input!="")
    {
        if(!isNumeric(input)) { alert('Not a number!'); return false; } 
        insertParam(elem, input)
        return true;
    }
    else {return false;}
}

function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

function insertParam(elem, value)
{
    elem.href=elem.href.concat('&budget='.concat(value));
}
