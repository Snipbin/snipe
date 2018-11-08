import uuid

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from simple_history.models import HistoricalRecords

from apps.account.models import SnipeUser
from apps.core.models import Language


class PrivacyChoices(object):
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'
    LINK = 'LINK'

    _choices = [
        (PUBLIC, "Visible to Everyone"),
        (PRIVATE, "Visible to Just Me"),
        (LINK, "Visible to People with Link"),
    ]

    @classmethod
    def choices(cls):
        return cls._choices


class Snippet(models.Model):
    title = models.CharField(max_length=128)
    language = models.ForeignKey(Language, related_name='snipes', on_delete=models.DO_NOTHING)
    description = models.TextField()
    code = models.TextField()
    author = models.ForeignKey(SnipeUser, related_name='snipes', on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    is_private = models.CharField(choices=PrivacyChoices.choices(), default='PUBLIC', max_length=16)
    created_at = models.DateTimeField()
    last_modified = models.DateTimeField()
    expiry_date = models.DateTimeField()
    _history_ = HistoricalRecords()

    def is_author_private(self):
        return self.is_private == 'PRIVATE'

    def __str__(self):
        return self.title


class Bookmark(models.Model):
    snippet = models.ForeignKey(Snippet, related_name='bookmarks', on_delete=models.CASCADE)
    user = models.ForeignKey(SnipeUser, related_name='bookmarks', on_delete=models.CASCADE)
    bookmarked_on = models.DateTimeField(default=timezone.now)

    class Meta(object):
        unique_together = ('snippet', 'user')


class SnippetViews(models.Model):
    snippet = models.ForeignKey(Snippet, related_name='views', on_delete=models.CASCADE)
    user = models.ForeignKey(SnipeUser, related_name='viewed_snipes', null=True, on_delete=models.SET_NULL)

    class Meta(object):
        unique_together = ('snippet', 'user')


class SnippetSearchUpdate(models.Model):
    snippet = models.ForeignKey(Snippet, null=True, blank=True, on_delete=models.SET_NULL)
    deletable_id = models.CharField(max_length=64, null=True, blank=True)
    pushed = models.BooleanField(default=False)


@receiver(post_save, sender=Snippet)
def snippet_post_save(sender, instance: Snippet, **kwargs):
    snippet_search = SnippetSearchUpdate(snippet=instance)
    snippet_search.save()


@receiver(post_delete, sender=Snippet)
def snippet_post_delete(sender, instance: Snippet, **kwargs):
    snippet_search = SnippetSearchUpdate(deletable_id=instance.uid)
    snippet_search.save()
