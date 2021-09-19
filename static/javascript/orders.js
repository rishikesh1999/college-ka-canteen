var  xhr=new XMLHttpRequest();
b=document.getElementById("orders")
function f (){
xhr.open("get","https://college-ka-canteen.herokuapp.com/ajax/")
xhr.onload=function(){
if(xhr.status == 200){
   dat=JSON.parse(xhr.responseText).v
  if(dat == 0){
document.getElementById("loginbutton").click()
  }
  else{
window.location.href="https://college-ka-canteen.herokuapp.com/orders/"


  }
}}

xhr.send();


}
b.addEventListener("click",f)
