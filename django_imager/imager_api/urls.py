from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from imager_api import views

urlpatterns = [
    url(r'^imager_api/$', views.ApiList.as_view()),
    url(r'^imager_api/(?P<pk>[0-9]+)/$', views.ApiDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
