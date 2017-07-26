from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.snippet.models import Snippet, PrivacyChoices


class SnippetEditSerializer(ModelSerializer):
    privacy = serializers.ChoiceField(choices=PrivacyChoices.choices(), source='is_private', write_only=True)
    expiry = serializers.ChoiceField(choices=[-1, 0, 7, 14, 30, 365], write_only=True)

    def save(self, **kwargs):
        self.validated_data.pop('expiry', None)
        return super().save(**kwargs)

    class Meta(object):
        model = Snippet
        exclude = ['author', 'created_at', 'expiry_date', 'last_modified']
