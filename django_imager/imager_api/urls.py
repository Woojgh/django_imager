from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from imager_api import views
from django.conf.urls import include

urlpatterns = [
    url(r'^imager_api/$', views.ApiList.as_view()),
    url(r'^imager_api/(?P<pk>[0-9]+)/$', views.ApiDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^$', views.api_root),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
