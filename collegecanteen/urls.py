"""shoppinglatest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from testapp import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home),
    path("myaccount/",views.myaccount),
    path("accounts/",include("django.contrib.auth.urls")),
    path("search/",views.search_view),
    path("view_img/<int:id>/",views.view_img),
    path("catogaries/<id>/",views.catogaries),
    path("post_comment/<int:id>/",views.post_comment),
    path("addtocart/<int:id>/",views.addtocart),
    path("ajax/",views.ajax),
    path("billing/",views.billing),
    path("update_cart/",views.update_cart),
    path("placeorder/",views.placeorder),
    path("payment/",views.payment),
    path("cancel/",views.cancel),
    path("orders/",views.view_orders),
    path("view_specific_order/<int:id>/",views.view_specific_order),
    path("forgot_password/",views.forgot_password),
    path("validate_user/",views.validate_user),

    path("validate_otp/",views.validate_otp),

    path("signup/",views.signup),
    path("college_chef/take_orders/",views.take_orders),
    path("college_chef/",views.college_chef),
    path("college_chef/view_orders_range/",views.view_orders_range),
    path("college_chef/chef_logout/",views.chef_logout),

    path("<cat>/<id>/",views.product_details),



]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
