from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET


CustomUser = get_user_model()
 
class Group(models.Model):
    name = models.CharField(max_length=100,)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name="joined_rooms")
    create_timestamp = models.DateTimeField(auto_now_add=True)
    grp_image = models.ImageField(upload_to="grp_image/", name="grp_image", null=True, blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(CustomUser, related_name="author_messages", on_delete=models.CASCADE)
    reciever = models.ForeignKey(CustomUser, related_name="reciever_messages", on_delete=models.CASCADE, null=True, blank=True)
    is_grp_msg = models.BooleanField()
    group = models.ForeignKey(Group, related_name="messages", on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}-{self.reciever.username}"

    def last_all_messages(cls, group):
        return cls.objects.filter(group__name=group).order_by("timestamp")[:]

    def get_user_messages(cls, user1, user2):
        return cls.objects.filter(
            Q(author=user1, receiver=user2) | Q(author=user2, receiver=user1)
        ).order_by("timestamp")

    def get_group_messages(cls, group_name):
        return cls.objects.filter(group__name=group_name, is_group_msg=True).order_by("timestamp")

    @login_required
    @require_GET
    def fetch_chat_history(request,reciever):
        sender_username = request.user.username
        receiver_username = request.GET.get(reciever, None)
        
        if receiver_username:
            messages = Message.get_user_messages(sender_username, receiver_username)
        else:
            group_name = request.GET.get('group', None)
            if group_name:
                messages = Message.get_group_messages(group_name)
            else:
                return JsonResponse({'error': 'Invalid request'}, status=400)
        
        serialized_messages = [{'author': msg.author.username, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]

        return JsonResponse({'messages': serialized_messages})
