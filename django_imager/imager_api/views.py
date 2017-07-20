from imager_api.models import Api
from imager_api.serializers import ApiSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User


class ApiList(generics.ListCreateAPIView):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ApiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
