
var dat;

var j;
function f(bn){
xhr.open("get","https://college-ka-canteen.herokuapp.com/ajax/")
xhr.onload=function(){
if(xhr.status == 200){
   dat=JSON.parse(xhr.responseText).v

  if(dat == 0){
document.getElementById("loginbutton").click()
  }
  else{

   j=bn.path[0].attributes.id.value.substring(9)
    xhr.open("post","https://college-ka-canteen.herokuapp.com/addtocart/"+j+"/")
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader("X-CSRFToken",document.cookie.substring(10))


    xhr.onload=function() {
if(xhr.status == 200){
  dat=JSON.parse(xhr.responseText)

    document.getElementById("cart").innerHTML=dat.cart_value
  document.getElementById("titletime"+j).innerHTML=dat.time
  document.getElementById("toastinner"+j).innerHTML="One "+dat.food_name +" added to your cart.."+"<a class='btn btn-success btn-sm' href='#'>Place Order</a>"


  $("#toast"+j).toast("show");
}


    }
    xhr.send('qty='+1)



  }
}
}

xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.setRequestHeader("X-CSRFToken",document.cookie.substring(10))
  xhr.send('name=rishwik&marks=70')
}

var v1=parseInt(document.getElementById("count_of_e").value)

for(var i=1;i<=v1;i++){
  alert(v1);
document.getElementById("addtocart"+i).addEventListener("click",f)


}
