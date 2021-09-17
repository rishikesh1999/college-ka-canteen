var  xhr=new XMLHttpRequest();

function f (){
xhr.open("POST","http://127.0.0.1:8000/validate_user/",true)
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.setRequestHeader("X-CSRFToken",document.cookie.substring(10))
xhr.onload=function(){
if(xhr.status == 200){
   dat=JSON.parse(xhr.responseText).v

  if(dat == 1){

  document.getElementById("submit_otp").type="submit"

  }
  else{
    document.getElementById("invalid_login_info_small").innerHTML=new Date()
    $("#invalid_login_info").toast("show")
    function f1(){
    $("#invalid_login_info").toast("hide")
    }
    setTimeout(f1,10000)

  }
}}
if(document.getElementById("id_username")==null){
  xhr.send("username="+document.getElementById("h3_username").innerHTML);


}else{
xhr.send("username="+document.getElementById("id_username").value);
document.getElementById("otp_info_small").innerHTML=new Date()
$("#otp_info").toast("show")
function f1(){
$("#otp_info").toast("hide")
}
setTimeout(f1,20000)

}

}
b=document.getElementById("send_otp")
b.addEventListener("click",f)
function f2(){
$("#otp_info").toast("hide")
}
document.getElementById("btn_close").addEventListener("click",f2)
document.getElementById("btn_close_otp").addEventListener("click",f2)
