from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.snippet.models import Snippet, privacy_choices


class SnippetEditSerializer(ModelSerializer):
    privacy = serializers.ChoiceField(choices=privacy_choices, source='is_private', write_only=True)
    expiry = serializers.ChoiceField(choices=[0, 7, 14, 30, 365], write_only=True)

    class Meta(object):
        model = Snippet
        exclude = ['author', 'created_at', 'expiry_date', 'last_modified']
