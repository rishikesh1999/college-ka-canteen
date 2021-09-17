from django.db import models
from django.contrib.auth.models import User

class foods(models.Model):
    fname=models.CharField(max_length=30)
    fquantity=models.IntegerField()
    fprice=models.IntegerField()
    fimg1=models.FileField()


    ftag1=models.CharField(max_length=30)
    ftag2=models.CharField(max_length=30,blank=True)


class cart(models.Model):
    user_id=models.ForeignKey(User,related_name="userid",on_delete=models.CASCADE)
    food_id=models.IntegerField()
    food_price=models.IntegerField()
    food_quantity=models.IntegerField()
    food_name=models.CharField(max_length=50)
class comments(models.Model):
    food_id=models.ForeignKey(foods,related_name="comments",on_delete=models.CASCADE)
    cdata=models.CharField(max_length=250)
    cemail=models.EmailField()
    cdate=models.DateTimeField(auto_now_add=True)
class orders(models.Model):
    order=models.TextField()
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    order_date=models.DateTimeField(auto_now_add=True)
    order_value=models.IntegerField()
    order_accepted=models.CharField(max_length=1,default='n')
    order_delivered=models.CharField(max_length=1,default='n')

class otp(models.Model):
    user_id=models.ForeignKey(User,related_name="otps",on_delete=models.CASCADE)
    odate=models.DateTimeField(auto_now_add=True)
    otp_value=models.CharField(max_length=6)
    otp_validated=models.CharField(max_length=1)
