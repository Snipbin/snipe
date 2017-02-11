from django.db import models
from simple_history.models import HistoricalRecords

from apps.account.models import UserProfile


class Snippet(models.Model):
    code = models.TextField()
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    _history_ = HistoricalRecords()
    author = models.ForeignKey(UserProfile, related_name="snippet")
