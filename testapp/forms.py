from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from testapp.models import otp
import datetime,pytz
class signup_modelform(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","password","email","first_name","last_name"]
class otp_form(forms.Form):
    username=forms.CharField()
    otp_value=forms.CharField(max_length=6)
    def is_valid1(self,r):
        u=User.objects.get(username=r.session.get("username"))
        self.ov=r.POST.get("otp_value")
        print("now otp value entered by user is  --->",self.ov)
        self.u=u
        flag=self.is_valid()
        print(self._errors.get("__all__"))
        if(self._errors.get("__all__") is None):
            return True
        else:
            return False
    def clean(self):
        o=otp.objects.filter(user_id=self.u.id).order_by("-odate","-id")
        o=o[0]
        print("now otp value entered by user is  --->",self.ov)
        print("otp value in databse is ",o.otp_value)
        print("first check passed",(pytz.utc.localize(datetime.datetime.now())-o.odate).seconds<68900)
        if((pytz.utc.localize(datetime.datetime.now())-o.odate).seconds<68900):
            print("second check passed",o.otp_value==self.ov)
            if(o.otp_value==self.ov):
                print("second check passed",o.otp_value==self.ov)
                return True
            else:
                raise ValidationError("Invalid Otp")
        else:
            raise ValidationError("Otp expired please try again later..")
        return True
class college_chef_form(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())
class orders_range(forms.Form):
    from_date=forms.DateField()
    to_date=forms.DateField()
