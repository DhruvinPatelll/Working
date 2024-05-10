from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to="profile_images/",
        name="profile_image", null=True, blank=True
    )
    create_timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "auth_user"

    def __str__(self):
        return self.username