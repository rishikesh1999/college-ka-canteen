from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.http import FileResponse,JsonResponse,HttpResponse
from testapp.models import foods,cart,comments,orders,otp
from django.contrib.auth.models import User
from django.db.models import Q,Sum,F
import datetime
from django.core.mail import send_mail
from django.template import loader
from django.core import serializers
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from testapp.forms import signup_modelform,otp_form,college_chef_form,orders_range
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from asgiref.sync import async_to_sync
from testapp import consumers
from channels.layers import get_channel_layer
from django.contrib.auth import logout
def user_log_in(r):
    u=authenticate(r,username=r.POST.get("username"),password=r.POST.get("password"))
    if(u is not None):
        login(r,u)
        return True
    else:
        return False
def home(r):
    if(r.user.id is not None):
        user_logged_in=True
        cart_value=cart.objects.filter(user_id=int(r.user.id)).aggregate(Sum("food_quantity")).get("food_quantity__sum")
        cart_value=0 if cart_value is None else cart_value
    else:
        user_logged_in=False
        cart_value=0
    if(r.method=="POST"):
        u=authenticate(r,username=r.POST.get("username"),password=r.POST.get("password"))
        if u is not None:
            login(r,u)
            return redirect("https://college-ka-canteen.herokuapp.com/myaccount/")
        else:
            invalid_user_flag=True
            return render(r,"home.html",{"user_logged_in":user_logged_in,"cart_value":cart_value,"invalid_user_flag":invalid_user_flag,"login_date":datetime.datetime.now()})


    return render(r,"home.html",{"user_logged_in":user_logged_in,"cart_value":cart_value})
def myaccount(r):
    if(r.user.id is not None):
        user_logged_in=True
        cart_value=cart.objects.filter(user_id=r.user.id).aggregate(Sum("food_quantity")).get("food_quantity__sum")
        cart_value=0 if cart_value is None else cart_value
        return render(r,"myaccount.html",{"user_logged_in":user_logged_in,"cart_value":cart_value})
    else:
        return redirect("https://college-ka-canteen.herokuapp.com")
def search_view(r):
    invalid_user_flag=False
    if(r.POST.get("username")==None or r.POST.get("password")==None):
        pass
    else:
        if(r.method=="POST"):
            u=authenticate(r,username=r.POST.get("username"),password=r.POST.get("password"))
            if u is not None:
                login(r,u)
                user_logged_in=True
                return redirect("https://college-ka-canteen.herokuapp.com/myaccount/")
            else:
                user_logged_in=False
                invalid_user_flag=True
    if(r.method=="POST"):
        user_logged_in=True if r.user.id is not None else False
        cart_value=cart.objects.filter(user_id=r.user.id).aggregate(Sum("food_quantity")).get("food_quantity__sum")
        cart_value=0 if cart_value is None else cart_value
        ts=r.POST.get("search","").lower()
        if(ts is not ""):
            e=foods.objects.filter(Q(fname__icontains=ts) | Q(ftag1__icontains=ts) | Q(ftag2__icontains=ts)).order_by("fname")
        else:
            e=foods.objects.all().order_by('-id')
        noflag=False if len(e)<1 else True
        pag=Paginator(e,20)
        page_number=r.GET.get("page")
        try:
            e_latest=pag.page(page_number)
        except PageNotAnInteger:
            e_latest=pag.page(1)
        except EmptyPage:
            e_latest=pag.page(paginator.num_pages)
        return render(r,"search_results.html",{"noflag":noflag,"food_items":e_latest,"user_logged_in":user_logged_in,"cart_value":cart_value,"invalid_user_flag":invalid_user_flag,"count_of_e":len(e)})
def view_img(r,id):
    i=foods.objects.filter(id=id)
    i=get_object_or_404(foods,id=id)
    return FileResponse(i.fimg1)
def catogaries(r,id):
    invalid_user_flag=False
    if(r.method=="POST"):
        u=authenticate(r,username=r.POST.get("username"),password=r.POST.get("password"))
        if u is not None:
            login(r,u)
            user_logged_in=True
            return redirect("https://college-ka-canteen.herokuapp.com/myaccount/")
        else:
            user_logged_in=False
            invalid_user_flag=True
    if(r.user.id is not None):
        main_temp="myaccount.html"
    else:
        main_temp="home.html"
    if(r.user.id is not None):
        cart_value=cart.objects.filter(user_id=int(r.user.id)).aggregate(Sum("food_quantity")).get("food_quantity__sum")
        cart_value=0 if cart_value is None else cart_value
    else:
        cart_value=0
    id=id.lower()
    e=foods.objects.filter(Q(ftag1__icontains=id)|Q(ftag2__icontains=id)).order_by("fname")
    pag=Paginator(e,20)
    page_number=r.GET.get("page")
    try:
        e_latest=pag.page(page_number)
    except PageNotAnInteger:
        e_latest=pag.page(1)
    except EmptyPage:
        e_latest=pag.page(paginator.num_pages)
    return render(r,"catogaries.html",{"food_items":e_latest,"main_temp":main_temp,"cart_value":cart_value,"invalid_user_flag":invalid_user_flag,"cat":id})
def product_details(r,cat,id):
    invalid_user_flag=False
    if(r.method=="POST"):
        u=authenticate(r,username=r.POST.get("username"),password=r.POST.get("password"))
        if u is not None:
            login(r,u)
        else:
            invalid_user_flag=True

    if(r.user.id is not None):
        user_logged_in=True
        c1=cart.objects.filter(food_id=id).aggregate(Sum("food_quantity")).get("food_quantity__sum")
        c1=1 if c1 is None else c1
    else:
        user_logged_in=False
        c1=1
    e=foods.objects.get(id=id)
    c=comments.objects.filter(food_id=e).order_by("-cdate","-id")
    if(r.user.id is not None):
        cart_value=cart.objects.filter(user_id=int(r.user.id)).aggregate(Sum("food_quantity")).get("food_quantity__sum")
        cart_value=0 if cart_value is None else cart_value

    else:
        cart_value=0
    return render(r,"product_details.html",{"food_item":e,"cat":cat,"comments":c,"number":len(c),"c":"comment","user_logged_in":user_logged_in,"value":c1,"cart_value":cart_value,"invalid_user_flag":invalid_user_flag,"login_date":datetime.datetime.now()})
def post_comment(r,id):
    if(r.method=="POST"):
        f1=foods.objects.get(id=id)
        c1=comments(cdata=r.POST.get("comment"),cemail=r.POST.get("email"),food_id=f1)

        c1.save()
        return redirect("https://college-ka-canteen.herokuapp.com/"+str(f1.ftag1)+"/"+str(f1.id)+"/")
def ajax(r):
    if r.user.id is None:
        return JsonResponse({"v":0})
    else:
        return JsonResponse({"v":1})
def addtocart(r,id):
    if(r.method=="POST"):
        if(r.user.id is not None):
            f=foods.objects.get(id=id)
            if(f.fquantity>=int(r.POST.get("qty"))):
                condition=cart.objects.filter(user_id=int(r.user.id)).filter(food_id=id)
                if(len(condition)<=0):
                    c=cart(food_name=f.fname,user_id=r.user._wrapped,food_id=f.id,food_price=f.fprice,food_quantity=int(r.POST.get("qty")))
                    c.save()
                else:
                    condition[0].food_quantity+=int(r.POST.get("qty"))
                    condition[0].save()
                s=datetime.datetime.now()
                s1=str(s.hour)+":"+str(s.minute)+":"+str(s.second)
                cart_value=cart.objects.filter(user_id=int(r.user.id)).aggregate(Sum("food_quantity")).get("food_quantity__sum")

                return JsonResponse({"food_name":f.fname.title(),"time":s1,"cart_value":cart_value})
        else:
            return redirect("https://college-ka-canteen.herokuapp.com")
def billing(r):
    if(r.user.id is not None):
        user_logged_in=True
        cart_value=cart.objects.filter(user_id=int(r.user.id)).aggregate(Sum("food_quantity")).get("food_quantity__sum")
        cart_value=0 if cart_value is None else cart_value

        c=cart.objects.filter(user_id=int(r.user.id)).filter(food_quantity__gt=0)
        total_value=cart.objects.filter(user_id=int(r.user.id)).aggregate(food_price__sum=Sum(F("food_price")*F("food_quantity"))).get("food_price__sum")
        return render(r,"billing.html",{"cart_items":c,"total_value":total_value,"user_logged_in":user_logged_in,"cart_value":cart_value})
    else:
        return redirect("https://college-ka-canteen.herokuapp.com")
def update_cart(r):
    if(r.user.id is not None):
        if(r.method=="POST"):
            delete_food_item=cart.objects.filter(user_id=int(r.user.id)).filter(food_id=int(r.POST.get("food_id")))
            delete_food_item.delete()
            user_logged_in=True
            cart_value=cart.objects.filter(user_id=int(r.user.id)).aggregate(Sum("food_quantity")).get("food_quantity__sum")
            cart_value=0 if cart_value is None else cart_value
            total_value=cart.objects.filter(user_id=int(r.user.id)).aggregate(food_price__sum=Sum(F("food_price")*F("food_quantity"))).get("food_price__sum")
            return JsonResponse({"total_value":total_value,"cart_value":cart_value})
    else:
        return redirect("https://college-ka-canteen.herokuapp.com")
def placeorder(r):
    if(r.method=="POST"):
        if(r.user.id is not None):
            user_logged_in=True
            c=cart.objects.filter(user_id=int(r.user.id))
            final_amount=cart.objects.filter(user_id=int(r.user.id)).aggregate(food_price__sum=Sum(F("food_price")*F("food_quantity"))).get("food_price__sum")
            final_total_items=cart.objects.filter(user_id=int(r.user.id)).aggregate(Sum("food_quantity")).get("food_quantity__sum")
            return render(r,"placeorder.html",{"user_logged_in":user_logged_in,"cart_value":final_total_items,"final_value":final_amount})
        else:
            return redirect("https://college-ka-canteen.herokuapp.com")
    else:
        return redirect("https://college-ka-canteen.herokuapp.com")
def payment(r):
    if(r.method=="POST"):
        if(r.user.id is not None):
            cart_items=cart.objects.filter(user_id=r.user.id)
            for x in cart_items:
                f=foods.objects.get(id=x.food_id)
                f.fquantity-=x.food_quantity
                f.save()
            order_info=serializers.serialize("json",cart_items)

            z=cart.objects.filter(user_id=r.user.id)
            final=z.aggregate(final_value=Sum(F("food_price")*F("food_quantity")),final_total_items=Sum("food_quantity"))
            o1=orders(user_id=r.user._wrapped,order=order_info,order_value=final["final_value"])
            o1.save()
            #email_html_message=loader.render_to_string("index.html")
            #send_mail("Order Info","order",fail_silently=True,html_message=email_html_message,recipient_list=[r.user.email],from_email="python4048#@gmail.com")
            chef_receive_msg={}
            chef_receive_msg["order_id"]=o1.id
            chef_receive_msg["order_date"]=str(o1.order_date)
            temp={}
            for x in cart_items:
                temp[x.food_name]=x.food_quantity

            chef_receive_msg["order"]=temp
            channel_layer = get_channel_layer()
            chef_receive_msg["new_order"]=1
            chef_receive_msg["c_from_a_to_d"]=0
            chef_receive_msg["delievery"]=0
            async_to_sync(channel_layer.group_send)("college_chef_accept_group", {
                'type': 'chat_message',
                'message': chef_receive_msg
            })
            cart_items.delete()
            cart_value=cart.objects.filter(user_id=r.user.id).aggregate(Sum("food_quantity")).get("food_quantity__sum")
            cart_value=0 if cart_value is None else cart_value
            user_logged_in=True
            return render(r,"thankyou.html",{"order_no":o1.id,"user_logged_in":user_logged_in,"cart_value":cart_value})
        else:
            return redirect("https://college-ka-canteen.herokuapp.com")
    else:
        return redirect("https://college-ka-canteen.herokuapp.com")
def cancel(r):
    if(r.method=="POST"):
        print(r.user.id ,"user id is")

        if(r.user.id is not None):
            user_logged_in=True

            cart_value=cart.objects.filter(user_id=int(r.user.id)).aggregate(Sum("food_quantity")).get("food_quantity__sum")
            cart_value=0 if cart_value is None else cart_value

            return render(r,"cancel.html",{"user_logged_in":user_logged_in,"cart_value":cart_value})
    else:
        return redirect("https://college-ka-canteen.herokuapp.com")

def view_orders(r):
    if(r.method=="POST"):
        status=user_log_in(r)
        if status==True:
            return redirect("https://college-ka-canteen.herokuapp.com/orders/")
        else:
            return render(r,"view_order.html",{"user_logged_in":False,"special_script":True,"first_login":0,"invalid_user_flag":True})
    if(r.user.id is not None):
        o=orders.objects.filter(user_id=r.user).order_by("-id")
        cart_value=cart.objects.filter(user_id=r.user.id).aggregate(Sum("food_quantity")).get("food_quantity__sum")
        cart_value=0 if cart_value is None else cart_value
        user_logged_in=True
        return render(r,"view_order.html",{"user_logged_in":user_logged_in,"cart_value":cart_value,"ordered":o,"special_script":False})
    else:
        return render(r,"view_order.html",{"user_logged_in":False,"special_script":True,"first_login":1})
def view_specific_order(r,id):
    if(r.user.id is not None):
        so=orders.objects.get(user_id=r.user.id,id=int(id))
        order_info=serializers.deserialize("json",so.order)
        cart_value=cart.objects.filter(user_id=r.user.id).aggregate(Sum("food_quantity")).get("food_quantity__sum")
        cart_value=0 if cart_value is None else cart_value
        user_logged_in=True
        return render(r,"view_specific_order.html",{"cart_value":cart_value,"user_logged_in":user_logged_in,"order_info":order_info,"so":so})
    else:
        return redirect("https://college-ka-canteen.herokuapp.com")
def signup(r):
    if(r.method=="POST"):
        if(r.POST.get("signup")=='1'):
            u=signup_modelform(r.POST)
            if(u.is_valid()):
                u1=User(username=u.cleaned_data["username"],password=u.cleaned_data["password"],email=u.cleaned_data["email"],last_name=u.cleaned_data["last_name"],first_name=u.cleaned_data["first_name"])
                u1.save()
                u1.set_password(u1.password)
                u1.save()
                return redirect("https://college-ka-canteen.herokuapp.com")
            else:
                return render(r,"signup.html",{"form":u})
        else:
            u=authenticate(r,username=r.POST.get("username"),password=r.POST.get("password"))
            if u is not None:
                login(r,u)
                return redirect("https://college-ka-canteen.herokuapp.com/myaccount/")
            else:
                invalid_user_flag=True
                return render(r,"home.html",{"user_logged_in":False,"cart_value":0,"invalid_user_flag":invalid_user_flag,"login_date":datetime.datetime.now()})
    return render(r,"signup.html",{"form":signup_modelform()})
def forgot_password(r):
    if(r.method=="POST"):
        return render(r,"otp.html",{"form":otp_form(),"otp_notsent_man":True})
    else:
        return redirect("https://college-ka-canteen.herokuapp.com")
def validate_user(r):
    if( r.method=="POST"):
        if(r.user.id is None):
            user=User.objects.filter(username=r.POST.get("username"))
            if(len(user)==1):
                user=user[0]
                new_otp1="abcdefghijk13mnopqrstuvwxyz24985670"
                new_l=[random.choice(new_otp1) for x in range(6)]
                new_otp=''.join(new_l)
                o=otp(user_id=user,otp_validated="n",otp_value=new_otp)
                o.save()
                #send_mail("Change Password","""Dear customer,\nYou tried to change password .If that is you please enter the below otp to change password.If that is not you please ignore it.\nOTP:"""+new_otp,from_email="python4048@gmail.com",recipient_list=[user.email,])
                r.session["username"]=r.POST.get("username")

                r.session.set_expiry(5000)
                return JsonResponse({"v":1})
            else:
                return JsonResponse({"v":0})
        else:
            user_logged_in=True
            cart_value=cart.objects.filter(user_id=int(r.user.id)).aggregate(Sum("food_quantity")).get("food_quantity__sum")
            cart_value=0 if cart_value is None else cart_value
            return render(r,"already_logged_in.html",{"user_logged_in":user_logged_in,"cart_value":cart_value})
    else:
        return redirect("https://college-ka-canteen.herokuapp.com")
def validate_otp(r):
    if(r.user.id is None):
        if(r.method=="POST"):
            if(r.session.get("username") is not None and otp.objects.filter(user_id=User.objects.get(username=r.session.get("username"))).order_by("-odate")[0].otp_validated=='y'):
                u1=User.objects.filter(username=r.session.get("username"))[0]
                o=otp.objects.filter(user_id=u1.id).order_by("-odate")
                if( o[0].otp_validated=='y'):
                    o.delete();
                    u=User.objects.filter(username=r.session.get("username"))
                    u=u[0]
                    u.set_password(r.POST.get("password"))
                    u.save()
                    return render(r,"successfull_password_update.html")
            else:
                o1=r.POST.get("otp_value")
                otp_validated=False
                u1=User.objects.filter(username=r.session.get("username"))
                u1=u1[0]
                o2=otp.objects.filter(user_id=u1.id).order_by("-odate")
                of1=otp_form(r.POST)
                if(of1.is_valid1(r)):
                    otp_validated=True
                    x=o2[0]
                    x.otp_validated="y"
                    x.save()

                    r.session.set_expiry(500)
                    return render(r,"change_password.html")
                else:
                    new_error_var=of1.errors.get("__all__")
                    return render(r,"otp.html",{"form":of1,"username":r.session.get("username"),"otp_sent_man":True,"otp_notsent_man":False,"errors":new_error_var})
        else:
            return redirect("https://college-ka-canteen.herokuapp.com")
    else:
        user_logged_in=True
        cart_value=cart.objects.filter(user_id=int(r.user.id)).aggregate(Sum("food_quantity")).get("food_quantity__sum")
        cart_value=0 if cart_value is None else cart_value
        return render(r,"already_logged_in.html",{"user_logged_in":user_logged_in,"cart_value":cart_value})

def college_chef(r):
    if(r.method=="POST"):
        f=college_chef_form(r.POST)
        if(f.is_valid()):
            u=authenticate(r,username=f.cleaned_data.get("username"),password=f.cleaned_data.get("password"))
            if(u is not None):
                login(r,u)
                return redirect("https://college-ka-canteen.herokuapp.com/college_chef/take_orders/")
        else:
            return render(r,"college_chef.html",{"form":f})
    else:
        return render(r,"college_chef.html",{"form":college_chef_form()})
@login_required
def take_orders(r):
    nao=orders.objects.filter(order_accepted="n").order_by('id')
    abndo=orders.objects.filter(order_accepted="y",order_delivered="n").order_by("id")
    for x in nao:
        x.order=serializers.deserialize("json",x.order)
    for x in abndo:
        x.order=serializers.deserialize("json",x.order)
    return render(r,"take_orders.html",{"nao":nao,"abndo":abndo})
@login_required
def view_orders_range(r):
    if(r.method=="POST"):
        f=orders_range(r.POST)
        if(f.is_valid()):
            o=orders.objects.filter(order_date__gte=f.cleaned_data["from_date"],order_date__lte=f.cleaned_data["to_date"])
            tov=orders.objects.filter(order_date__gte=f.cleaned_data["from_date"],order_date__lte=f.cleaned_data["to_date"]).aggregate(Sum("order_value"))
            return render(r,"previos_orders.html",{"form":f,"orders":o,"tov":tov["order_value__sum"],"tno":len(o)})
        else:
            return render(r,"previos_orders.html",{"form":f})
    else:
        return render(r,"previos_orders.html",{"form":orders_range()})
def chef_logout(r):
    logout(r)
    return redirect("https://college-ka-canteen.herokuapp.com/college_chef/take_orders/")
