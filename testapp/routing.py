from django.urls import path

from testapp import consumers

websocket_urlpatterns = [

    path("ws/college_chef/accept_order/",consumers.college_chef_consumer.as_asgi())
]
