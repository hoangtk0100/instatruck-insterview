from .repository import MovieRepo, ActorRepo, DirectorRepo
from rest_framework.decorators import api_view
from .util.utils import catch_exceptions
from .util.base import BaseResponse
from .util.exceptions import InvalidArgumentException
from .util.messages import NEGATIVE_ID

@api_view(['GET'])
@catch_exceptions
def list_movies(request):
    '''
    # List all movies
    '''
    movies = MovieRepo.list()
    data = list(map(lambda item: item.to_dict(), movies))
    return BaseResponse(data=data)

@api_view(['GET'])
@catch_exceptions
def list_movies_by_actor(request, id):
    '''
    # List all movies by actor
    '''
    _validate_id(id)
    
    actor = ActorRepo.get_by_id(id)
    movies = MovieRepo.list_by_actor(actor)
    data = list(map(lambda item: item.to_dict(), movies))
    return BaseResponse(data=data)

@api_view(['GET'])
@catch_exceptions
def list_movies_by_director(request, id):
    '''
    # List all movies by director
    '''
    _validate_id(id)
    
    director = DirectorRepo.get_by_id(id)
    movies = MovieRepo.list_by_director(director)
    data = list(map(lambda item: item.to_dict(), movies))
    return BaseResponse(data=data)

@api_view(['GET'])
@catch_exceptions
def list_actors(request):
    '''
    # List all movies
    '''
    actors = ActorRepo.list()
    data = list(map(lambda item: item.to_dict(), actors))
    return BaseResponse(data=data)

@api_view(['GET'])
@catch_exceptions
def list_directors(request):
    '''
    # List all movies
    '''
    directors = DirectorRepo.list()
    data = list(map(lambda item: item.to_dict(), directors))
    return BaseResponse(data=data)

def _validate_id(id):
    if id < 1:
        raise InvalidArgumentException(NEGATIVE_ID)
