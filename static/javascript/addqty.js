x=document.getElementById("qty")
b1=document.getElementById("incqty")
b2=document.getElementById("decqty")
function binc(){
  if(x.value<10){

    x.value=parseInt(x.value) + 1;
  }
}
function bdec(){
  if(x.value>0){

    x.value=x.value-1;
  }
}
b1.addEventListener("click",binc)
b2.addEventListener("click",bdec)
