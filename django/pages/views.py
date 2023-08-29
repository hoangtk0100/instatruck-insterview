from util.apis import paginate_data, catch_exceptions, short_convert_string_to_date
from .filter import MovieFilter, BestMovieFilter, ActorFilter
from .serializers import MovieSerializer, ActorSerializer
from rest_framework.decorators import action
from util.base import BaseResponse
from util.views import BaseView
from .models import Movie, Actor

class MovieView(BaseView):

    serializer_classes = {
        'filter': MovieSerializer,
        'filter_bests': MovieSerializer,
    }

    @action(methods=['GET'], detail=False, url_path='movies')
    @catch_exceptions
    def filter(self, request):
        '''
        # Options
            @page: Optional - Default = 1
            @limit: Optional - Default = 10
            
            @start_year: Optional
            @end_year: Optional

            @actor_id: Optional
            @actor_name: Optional

            @director_id: Optional
            @director_name: Optional

        '''
        queryset = Movie.objects.all()
        queryset = MovieFilter(request.GET, queryset=queryset).qs

        serializer = self.get_serializer(queryset, many=True)
        return BaseResponse(data=paginate_data(request, serializer.data))

    @action(methods=['GET'], detail=False, url_path=r'movies/best/(?P<amount>\d+)')
    @catch_exceptions
    def filter_bests(self, request, amount):
        '''
        # Options
            @page: Optional - Default = 1
            @limit: Optional - Default = 10
            
            @start_year: Optional
            @end_year: Optional

            @actor_id: Optional
            @actor_name: Optional

            @director_id: Optional
            @director_name: Optional

            @sort_by: Optional [any movie|actor|director fields]
            @sort_type: Optional [asc | desc]

        '''
        request.GET._mutable = True
        request.GET['limit'] = amount
        request.GET._mutable = False

        queryset = Movie.objects.all()
        queryset = BestMovieFilter(request.GET, queryset=queryset).qs

        serializer = self.get_serializer(queryset, many=True)
        return BaseResponse(data=paginate_data(request, serializer.data))


class ActorView(BaseView):

    serializer_classes = {
        'filter_date': ActorSerializer,
    }

    @action(methods=['GET'], detail=False, url_path=r'actors/birthdays/(?P<date>\d+)')
    @catch_exceptions
    def filter_date(self, request, date):
        '''
        # Options
            @page: Optional - Default = 1
            @limit: Optional - Default = 10
        '''
        request.GET._mutable = True
        request.GET['search'] = date
        request.GET._mutable = False

        queryset = Actor.objects.all()
        queryset = ActorFilter(request.GET, queryset=queryset).qs

        serializer = self.get_serializer(queryset, many=True)
        sorted_records = sorted(serializer.data, key=lambda actor: _absolute_date_difference(date, actor))
        return BaseResponse(data=paginate_data(request, sorted_records))


def _absolute_date_difference(target_date, actor):
    target_datetime = short_convert_string_to_date(target_date)
    actor_datetime = short_convert_string_to_date(actor['date'])
    return abs((actor_datetime - target_datetime).days)