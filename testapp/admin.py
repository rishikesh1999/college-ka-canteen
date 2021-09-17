from django.contrib import admin
from testapp.models import cart,foods,comments,orders,otp
class admin_foods(admin.ModelAdmin):

    list_display=["fname","fquantity","fprice"]
class admin_cart(admin.ModelAdmin):
    list_display=["user_id","food_id","food_quantity","food_price","food_name"]
class admin_comments(admin.ModelAdmin):
    list_display=["cemail","cdata","cdate"]
class admin_orders(admin.ModelAdmin):
    list_display=["id","user_id","order","order_value"]
class admin_otp(admin.ModelAdmin):
    list_display=["user_id","odate","otp_value"]
admin.site.register(cart,admin_cart)
admin.site.register(foods,admin_foods)
admin.site.register(comments,admin_comments)
admin.site.register(orders,admin_orders)
admin.site.register(otp,admin_otp)
