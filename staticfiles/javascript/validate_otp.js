var  xhr=new XMLHttpRequest();

function f (){
xhr.open("POST","https://college-ka-canteen.herokuapp.com/validate_otp/",true)
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.setRequestHeader("X-CSRFToken",document.cookie.substring(10))
xhr.onload=function(){
if(xhr.status == 200){
   dat=JSON.parse(xhr.responseText).v

  if(dat == 1){
  document.getElementById("otp_value").type="text"
  document.getElementById("submit_otp").type="submit"

  }
  else{


  }
}}
xhr.send("username="+document.getElementById("user_id").value);
}
b=document.getElementById("send_otp")
b.addEventListener("click",f)
