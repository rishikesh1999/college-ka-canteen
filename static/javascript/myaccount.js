var  xhr=new XMLHttpRequest();

b=document.getElementById("myaccount")
function f (){
xhr.open("get","http://127.0.0.1:8000/ajax/")
xhr.onload=function(){
if(xhr.status == 200){
   dat=JSON.parse(xhr.responseText).v
  if(dat == 0){
document.getElementById("loginbutton").click()
  }
  else{
window.location.href="http://127.0.0.1:8000/myaccount/"
  }
}}

xhr.send();


}
b.addEventListener("click",f)
