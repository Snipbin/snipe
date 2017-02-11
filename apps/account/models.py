from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    picture = None
    organisation = models.CharField(max_length=256)
    designation = models.CharField(max_length=256)

    def __str__(self):
        return self.user.username
