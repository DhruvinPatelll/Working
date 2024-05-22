from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

CustomUser = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name="joined_rooms")
    create_timestamp = models.DateTimeField(auto_now_add=True)
    grp_image = models.ImageField(upload_to="grp_image/", null=True, blank=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    author = models.ForeignKey(CustomUser, related_name="author_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="receiver_messages", on_delete=models.CASCADE, null=True, blank=True)
    is_grp_msg = models.BooleanField()
    group = models.ForeignKey(Group, related_name="messages", on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    @classmethod
    def last_all_messages(cls, group):
        return cls.objects.filter(group__name=group).order_by("timestamp")

    @classmethod
    def get_user_messages(cls, user1, user2):
        return cls.objects.filter(
            Q(author=user1, receiver=user2) | Q(author=user2, receiver=user1)
        ).order_by("timestamp")

    @classmethod
    def get_group_messages(cls, group_name):
        return cls.objects.filter(group__name=group_name, is_grp_msg=True).order_by("timestamp")
    
