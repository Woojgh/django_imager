from rest_framework import serializers
from imager_api.models import Api, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class ApiSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='imager_api-highlight', format='html')

    class Meta:
        model = Api
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    imager_api = serializers.HyperlinkedRelatedField(many=True, view_name='imager_api-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'imager_api')
