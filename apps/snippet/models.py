import uuid

from django.db import models
from simple_history.models import HistoricalRecords

from apps.account.models import SnipeUser
from apps.core.models import Language


class Snippet(models.Model):
    title = models.CharField(max_length=64)
    language = models.ForeignKey(Language, related_name='snipes')
    description = models.TextField()
    code = models.TextField()
    author = models.ForeignKey(SnipeUser, related_name='snipes')
    uid = models.UUIDField(default=uuid.uuid4, unique=True)  # TODO: Make a method to generate UUID
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    last_modified = models.DateTimeField()
    expiry_date = models.DateTimeField()
    _history_ = HistoricalRecords()

    def __str__(self):
        return self.title
