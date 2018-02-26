from .models import Link
from rest_framework import serializers


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('creation_date', 'link_displays', )


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('path', 'file', 'my_user')
