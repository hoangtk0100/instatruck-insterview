from util.filters import YearRangeParamsFilter
from util.exceptions import ValidationException
from util.messages import SORT_TYPE_NOT_SUPPORT
from util.apis import get_sort_type
from django.db.models import Q
from .models import Movie
import django_filters

class MovieFilter(YearRangeParamsFilter):
    class Meta:
        model = Movie
        ordering = ['name']
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
    

class BestMovieFilter(YearRangeParamsFilter):
    class Meta:
        model = Movie
        ordering = ['-rating', '-metascore']
        fields = '__all__'

    sort_by = django_filters.CharFilter(method='sort_by_filter') 

    actor_id = django_filters.NumberFilter(method='actor_filter')
    actor_name = django_filters.CharFilter(method='actor_filter')

    director_id = django_filters.NumberFilter(method='director_filter')
    director_name = django_filters.CharFilter(method='director_filter')

    def sort_by_filter(self, queryset, name, value):
        '''
        # Filter word in char (icontains)
        @name: default - 'sort_by'
        @value: received from the request
        '''
        sort_type = self.data.get('sort_type', 'asc')
        if sort_type and (sort_type.lower() not in ['asc', 'desc']):
            raise ValidationException(SORT_TYPE_NOT_SUPPORT)

        if not value:
            value = '-rating'
        else:
            if 'actor_' in value:
                value = value.replace('actor_', 'actor__')
            elif 'director_' in value:
                value = value.replace('director_', 'director__')

        return queryset.order_by(get_sort_type(sort_type) + value)

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