from django.db import models
from simple_history.models import HistoricalRecords

from apps.account.models import UserProfile
from apps.core.models import Language


class Snippet(models.Model):
    title = models.CharField(max_length=64)
    language = models.ForeignKey(Language, related_name='snip_lang')
    code = models.TextField()
    author = models.ForeignKey(UserProfile, related_name="snip_author")
    uid = models.CharField(max_length=32)
    is_private = models.BooleanField(default=False)
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    expiry_date = models.DateTimeField()
    _history_ = HistoricalRecords()

    def __str__(self):
        return self.title
