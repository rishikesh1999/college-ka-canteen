lg=document.getElementById("loginbutton")
fl=document.getElementById("first_login").value
if(fl==0){
  $("#invalid").toast("show")
  function f(){

  $("#invalid").toast("hide")
  document.getElementById("login_form").setAttribute("action","http://127.0.0.1:8000/orders/")
  lg.click()}



  setTimeout(f,2000)

}
else{
document.getElementById("login_form").setAttribute("action","http://127.0.0.1:8000/orders/")
lg.click()}
