
from django.urls import path
from . import apis
from .views import MovieView, ActorView

from rest_framework import routers
router = routers.DefaultRouter(trailing_slash=False)
router.register('', MovieView, basename='')
router.register('', ActorView, basename='')
urlpatterns = router.urls

urlpatterns.extend([
    path('actors', apis.list_actors, name = 'List actors'),
    path('actors/<int:id>/films', apis.list_movies_by_actor, name = 'List films for actor'),

    path('directors', apis.list_directors, name = 'List directors'),
    path('directors/<int:id>/films', apis.list_movies_by_director, name = 'List films for director'),
])
