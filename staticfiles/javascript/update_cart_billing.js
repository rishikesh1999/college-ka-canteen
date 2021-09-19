var xhr=new XMLHttpRequest();
function remove(food_id){
  food_id=food_id.target.id.substring(6)

xhr.open("post","https://college-ka-canteen.herokuapp.com/update_cart/")
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.setRequestHeader("X-CSRFToken",document.cookie.substring(10))
xhr.onload=function(){
  if(xhr.status == 200){
    result=JSON.parse(xhr.responseText)
    document.getElementById("food_item_block"+food_id).remove()
    document.getElementById("final_value").innerHTML=result.total_value
    document.getElementById("final_count").innerHTML=result.cart_value
    document.getElementById("cart").innerHTML=result.cart_value
if(result.total_value == null){

document.getElementById("final_place_order").remove();
document.getElementById("final_count_main").innerHTML="No items present in cart";

document.getElementById("final_value_main").remove();


}
  }



}
xhr.send("food_id="+food_id)
}
var x1=document.getElementsByClassName("food_item_block")

for(i=0;i<x1.length;i++){
var temp=x1[i].id.substr(15)
document.getElementById("delete"+temp).addEventListener("click",remove);
}
