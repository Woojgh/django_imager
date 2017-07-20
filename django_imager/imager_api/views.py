from imager_api.models import Api
from imager_api.serializers import ApiSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from imager_api.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers


class ApiList(generics.ListCreateAPIView):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ApiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'imager_api': reverse('imager_api-list', request=request, format=format)
    })


class SnippetHighlight(generics.GenericAPIView):
    queryset = Api.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        imager_api = self.get_object()
        return Response(imager_api.highlighted)
