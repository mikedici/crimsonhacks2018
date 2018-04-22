

var changeimage = document.getElementById('myImage');
var dropdownvalues = document.getElementsByClassName("dropdown-content");


function myfunction(word){
    if(word==="Bitcoin")
       //changeimage.src="bitcoin.png";
       document.getElementById('myImage').src="bitcoin.png";

    if(word==="Zcash")
    document.getElementById('myImage').src="zcash.png";
    
    if(word==="Litecoin")
    document.getElementById('myImage').src="Litecoin.png";
      
    if(word==="Etherium")
    document.getElementById('myImage').src="etherium.png";

    if(word==="Barchart")
    document.getElementById('myImage').src="barchart.png";

    if(word==="Crypto")
    document.getElementById('myImage').src="Crypto-sentiment.png";
    
}
