# chat/consumers.py
import json,datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from testapp.models import orders

class college_chef_consumer(WebsocketConsumer):
    def connect(self):
        self.user=self.scope["user"]
        
        if(self.user.is_authenticated):
            async_to_sync(self.channel_layer.group_add)("college_chef_accept_group",self.channel_name)
            self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            "college_chef_accept_group",
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        json_data=json.loads(text_data)
        print("this is insdie resceive",json_data)
        if(json_data.get("c_from_a_to_d")==1):
            order1=orders.objects.get(id=json_data["order_id"])
            order1.order_accepted="y"
            print(order1.order_delivered)
            order1.save()
            order_id=json_data["order_id"]
            self.send(text_data=json.dumps({'order_id':order_id,"new_order":0,"c_from_a_to_d":1,"delivery":0}))
        else:
            order1=orders.objects.get(id=json_data["order_id"][1:])
            order1.order_delivered="y"
            order1.save()
            order_id=json_data["order_id"][1:]
            self.send(text_data=json.dumps({"order_id":order_id,"new_order":0,"c_from_a_to_d":0,"delivery":1}))
    def chat_message(self, event):
        message = event["message"]
        print("this is chat_message")
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,}
        ))
