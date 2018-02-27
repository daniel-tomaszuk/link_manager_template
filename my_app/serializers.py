from .models import Link
from rest_framework import serializers
from django.contrib.auth.models import User


class InfoSerializer(serializers.ModelSerializer):
    """
    Serializes data about secured content (Link model object)
    """
    class Meta:
        model = Link
        fields = ('creation_date', 'link_displays', 'valid', 'my_user')


class ContentSerializer(serializers.ModelSerializer):
    """
    Serialize POST'ed content. Add user the the content.
    """
    my_user = serializers.ReadOnlyField(source='my_user.username')

    class Meta:
        model = Link
        fields = ('path', 'file', 'my_user',)


class UserSerializer(serializers.ModelSerializer):
    """
    Serialize user info.
    """
    class Meta:
        model = User
        fields = '__all__'
