
from django.urls import path
from . import apis

urlpatterns = [
    path('movies', apis.list_movies, name = 'List movies'),
    
    path('actors', apis.list_actors, name = 'List actors'),
    path('actors/<int:id>/films', apis.list_movies_by_actor, name = 'List films for actor'),

    path('directors', apis.list_directors, name = 'List directors'),
    path('directors/<int:id>/films', apis.list_movies_by_director, name = 'List films for director'),
]
