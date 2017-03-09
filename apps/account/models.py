from django.contrib.auth.models import User, AbstractUser
from django.db import models


class SnipeUser(AbstractUser):
    """
    username is AAD object_id
    """

    object_id = models.CharField(max_length=64)
    tenant_id = models.CharField(max_length=64)
    refresh_token = models.TextField(null=True, blank=True)

    job_title = models.CharField(max_length=256, null=True, blank=True)
    department = models.CharField(max_length=256, null=True, blank=True)
    picture = models.ImageField(null=True, blank=True)

    # @property
    # def is_authenticated(self):
    #     return True
