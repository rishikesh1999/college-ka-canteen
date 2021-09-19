lg=document.getElementById("loginbutton")
fl=document.getElementById("first_login").value
if(fl==0){
  $("#invalid").toast("show")
  function f(){

  $("#invalid").toast("hide")
  document.getElementById("login_form").setAttribute("action","https://college-ka-canteen.herokuapp.com/orders/")
  lg.click()}



  setTimeout(f,2000)

}
else{
document.getElementById("login_form").setAttribute("action","https://college-ka-canteen.herokuapp.com/orders/")
lg.click()}
