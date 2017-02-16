from django.db import models
from simple_history.models import HistoricalRecords

from apps.account.models import UserProfile


LANGUAGE_CHOICES = (
    (1, "C#"),
    (2, "PowerShell"),
    (3, "C++"),
    (4, "Python"),
    (5, "Rust"),
    (6, "JavaScript"),
    (7, "CSS"),
)


class Snippet(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    language = models.IntegerField(choices=LANGUAGE_CHOICES, default=1)
    code = models.TextField()
    author = models.ForeignKey(UserProfile, related_name="snippet")
    uid = models.CharField(max_length=32)
    is_private = models.BooleanField(default=False)
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    expiry_date = models.DateTimeField()
    _history_ = HistoricalRecords()

    def __str__(self):
        return self.title
