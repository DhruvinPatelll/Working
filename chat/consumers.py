from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Group
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        group_name = data['group_name']
        messages = Message.last_all_messages(group_name)
        content = {"command": "messages", "messages": self.messages_to_json(messages)}
        self.send_message(content)

    def new_message(self, data):
        author = self.scope["user"]
        message_content = data["message"]
        group_name = data.get("group_name")
        is_grp_msg = data.get("is_grp_msg", False)

        if is_grp_msg:
            group = Group.objects.get(name=group_name)
            message = Message.objects.create(author=author, content=message_content, group=group, is_grp_msg=True)
        else:
            receiver_username = data["receiver"]
            receiver = CustomUser.objects.get(username=receiver_username)
            message = Message.objects.create(author=author, content=message_content, receiver=receiver, is_grp_msg=False)

        content = {"command": "new_message", "message": self.message_to_json(message)}
        self.send_chat_message(content)

    def messages_to_json(self, messages):
        return [self.message_to_json(message) for message in messages]

    def message_to_json(self, message):
        return {
            "author": message.author.username,
            "content": message.content,
            "timestamp": str(message.timestamp),
            "is_grp_msg": message.is_grp_msg
        }

    commands = {"fetch_messages": fetch_messages, "new_message": new_message}

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.room_group_name = f"chat_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))
