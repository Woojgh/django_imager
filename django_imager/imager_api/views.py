from imager_api.models import Api
from imager_api.serializers import ApiSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from imager_api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """This views will provide `list` and `detail` actions."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiViewSet(viewsets.ModelViewSet):
    """This will be the view for our Api sets and it includes higlighting."""
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        api = self.get_object()
        return Response(api.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
