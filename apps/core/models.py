from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=64)
    extensions = models.TextField(null=True, blank=True)
    css_style = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.name
