var xhr=new XMLHttpRequest()
var dat,q;
var flag=0;

atc=document.getElementById("addtocart")
function f(){
xhr.open("get","https://college-ka-canteen.herokuapp.com/ajax/")
xhr.onload=function(){
if(xhr.status == 200){
   dat=JSON.parse(xhr.responseText).v

  if(dat == 0){
document.getElementById("loginbutton").click()
  }
  else{
    xhr.open("post","https://college-ka-canteen.herokuapp.com/addtocart/"+document.getElementById("productid").getAttribute("action").charAt(50)+"/")
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader("X-CSRFToken",document.cookie.substring(10))
    q=document.getElementById("qty").value

    xhr.onload=function() {
if(xhr.status == 200){
  dat=JSON.parse(xhr.responseText)

    document.getElementById("cart").innerHTML=dat.cart_value
  document.getElementById("titletime").innerHTML=dat.time
  document.getElementById("toastinner").innerHTML=dat.food_name +"  Quantity("+q+") added to your cart.."+"<a class='btn btn-success btn-sm' href='https://college-ka-canteen.herokuapp.com/billing/'>Place Order</a>"


  $(".toast").toast("show");
  if(flag==1){
    window.location.href="https://college-ka-canteen.herokuapp.com/billing/"
  }
}


    }
    xhr.send('qty='+q)



  }
}
}

xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.setRequestHeader("X-CSRFToken",document.cookie.substring(10))
  xhr.send('name=rishwik&marks=70')
}
atc.addEventListener("click",f)
buy =document.getElementById("buynow")
flag=0
function g(){
atc.click()
flag=1;


}

buy.addEventListener("click",g)
