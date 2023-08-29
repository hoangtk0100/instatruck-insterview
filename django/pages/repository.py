from .models import Movie, Actor, Director
from .util.exceptions import NotFoundException
from .util.messages import ACTOR_NOT_FOUND, DIRECTOR_NOT_FOUND

class MovieRepo:
    @staticmethod
    def list():
        '''
        # List all movies
        '''
        try:
            return Movie.objects.filter().order_by('title')
        except Exception:
            return []
        
    @staticmethod
    def list_by_actor(actor):
        '''
        # List all movies by actor
        '''
        try:
            return Movie.objects.filter(actor=actor).order_by('title')
        except Exception:
            return []
    
    @staticmethod
    def list_by_director(director):
        '''
        # List all movies by director
        '''
        try:
            return Movie.objects.filter(director=director).order_by('title')
        except Exception:
            return []


class ActorRepo:
    @staticmethod
    def list():
        '''
        # List all actors
        '''
        try:
            return Actor.objects.filter().order_by('name')
        except Exception:
            return []

    @staticmethod
    def get_by_id(id):
        '''
        # Get actor by id
        '''
        try:
            return Actor.objects.get(id=id)
        except Exception:
            raise NotFoundException(ACTOR_NOT_FOUND)


class DirectorRepo:
    @staticmethod
    def list():
        '''
        # List all directors
        '''
        try:
            return Director.objects.filter().order_by('name')
        except Exception:
            return []
        
    @staticmethod
    def get_by_id(id):
        '''
        # Get director by id
        '''
        try:
            return Director.objects.get(id=id)
        except Exception:
            raise NotFoundException(DIRECTOR_NOT_FOUND)
        