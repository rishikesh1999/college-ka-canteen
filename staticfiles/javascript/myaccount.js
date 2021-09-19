var  xhr=new XMLHttpRequest();

b=document.getElementById("myaccount")
function f (){
xhr.open("get","https://college-ka-canteen.herokuapp.com/ajax/")
xhr.onload=function(){
if(xhr.status == 200){
   dat=JSON.parse(xhr.responseText).v

  if(dat == 0){
document.getElementById("loginbutton").click()
  }
  else{
window.location.href="https://college-ka-canteen.herokuapp.com/myaccount/"

  }
}}

xhr.send();


}
b.addEventListener("click",f)
