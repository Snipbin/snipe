from rest_framework import serializers

from apps.search.models import AzureSearchResponseData, AzureSearchResponse


class SearchUpdateSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["upload", "delete"], default="upload")
    id_ = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    code = serializers.CharField()
    author = serializers.CharField()
    language = serializers.CharField()

    def to_representation(self, instance):
        initial = super().to_representation(instance)
        initial["@value.action"] = initial["action"]
        initial["id"] = initial["id_"]
        del initial["action"]
        del initial["id_"]
        return initial


class AzureSearchResponseDataSerializer(serializers.Serializer):
    score = serializers.FloatField()
    id_ = serializers.CharField()

    def to_internal_value(self, data):
        data['score'] = data['@search.score']
        data['id_'] = data['id']
        return super().to_internal_value(data)

    def create(self, validated_data):
        return AzureSearchResponseData(**validated_data)

    class Meta(object):
        fields = '__all__'


class AzureSearchResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    value = AzureSearchResponseDataSerializer(many=True)

    def to_internal_value(self, data):
        data['count'] = data['@odata.count']
        return super().to_internal_value(data)

    def create(self, validated_data):
        return AzureSearchResponse(**validated_data)

    class Meta(object):
        fields = '__all__'
