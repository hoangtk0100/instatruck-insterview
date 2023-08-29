from .serializers import MovieSerializer
from rest_framework.decorators import action
from .filter import MovieFilter, BestMovieFilter
from util.views import BaseView
from util.apis import paginate_data, catch_exceptions
from util.base import BaseResponse
from .models import Movie

class MovieView(BaseView):

    serializer_classes = {
        'filter': MovieSerializer,
        'get_best': MovieSerializer,
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
    def get_best(self, request, amount):
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