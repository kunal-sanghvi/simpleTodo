from django.urls import path, re_path

from .views import list_todo, create_todo, delete_todo


urlpatterns = [
    path('', list_todo),
    re_path(r'^create/$', create_todo),
    re_path(r'^(?P<pk>\d+)/$', delete_todo),
]
