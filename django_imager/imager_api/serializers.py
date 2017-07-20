from rest_framework import serializers
from imager_api.models import Api, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class ApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Api
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Api.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets', 'owner')
