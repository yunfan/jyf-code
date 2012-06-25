/**
 *  This is an funny code for bones7456
 *  he want to give those who use trident engine for web viewing 
 *
 *  Author: jyf<jyf1987@gmail.com>
 *  Date: 2010-04-15
 *  License: do anything you want to do to it
**/
fucntion warnIE(){
    var ie = !-[1,];
    if(ie){
        o = document.createElement("DIV");
        pa = document.getElementsByTagName("body")[0];
        o.id = "warnie";   // you need to define its style to this in css
        text = document.createTextNode("Fail, why are you still using IE? man");
        o.appendChild(text);
        pa.appendChild(o)
    }
}

document.body.attachEvent('onload', warnIE);
