from .serializers import MovieSerializer
from rest_framework.decorators import action
from .filter import MovieFilter
from util.views import BaseView
from util.apis import paginate_data, catch_exceptions
from util.base import BaseResponse
from .models import Movie

class MovieView(BaseView):

    serializer_classes = {
        'filter': MovieSerializer,
    }

    # Use POST method for complex query, refer than GET with params
    @action(methods=['POST'], detail=False, url_path='movies')
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
        queryset = MovieFilter(request.data, queryset=queryset).qs

        data = list(map(lambda item: item.to_dict(), queryset))
        return BaseResponse(data=paginate_data(request, data))