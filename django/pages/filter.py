from util.filters import YearRangeParamsFilter
from django.db.models import Q
from .models import Movie
import django_filters

class MovieFilter(YearRangeParamsFilter):
    class Meta:
        model = Movie
        fields = '__all__'

    actor_id = django_filters.NumberFilter(method='actor_filter')
    actor_name = django_filters.CharFilter(method='actor_filter')

    director_id = django_filters.NumberFilter(method='director_filter')
    director_name = django_filters.CharFilter(method='director_filter')

    def actor_filter(self, queryset, name, value):
        '''
        # Filter by actor
        @name: default - [actor_id, actor_name]
        @value: received from the request
        '''
        if (name == 'actor_id'):
            return queryset.filter(
                Q(actor__id=value)
            )

        name = name.replace('actor_', 'actor__')
        return queryset.filter(**{
            name + '__icontains': value
        })
    
    def director_filter(self, queryset, name, value):
        '''
        # Filter by director
        @name: default - [director_id, director_name]
        @value: received from the request
        '''
        if (name == 'director_id'):
            return queryset.filter(
                Q(director__id=value)
            )

        name = name.replace('director_', 'director__')
        return queryset.filter(**{
            name + '__icontains': value
        })