from django.db.models import Q, F, ExpressionWrapper, IntegerField
from util.apis import get_sort_type, convert_string_to_date
from util.filters import YearRangeParamsFilter, FilterSet
from django_filters import NumberFilter, CharFilter
from util.exceptions import ValidationException
from util.messages import SORT_TYPE_NOT_SUPPORT
from django.db.models.functions import Abs
from util.constants import DDMMYYY
from .models import Movie, Actor

class MovieFilter(YearRangeParamsFilter):
    class Meta:
        model = Movie
        ordering = ['name']
        fields = '__all__'

    actor_id = NumberFilter(method='actor_filter')
    actor_name = CharFilter(method='actor_filter')

    director_id = NumberFilter(method='director_filter')
    director_name = CharFilter(method='director_filter')

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

    sort_by = CharFilter(method='sort_by_filter') 

    actor_id = NumberFilter(method='actor_filter')
    actor_name = CharFilter(method='actor_filter')

    director_id = NumberFilter(method='director_filter')
    director_name = CharFilter(method='director_filter')

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


class ActorFilter(FilterSet):
    class Meta:
        model = Actor
        fields = '__all__'

    search = CharFilter(method='search_filter')

    def search_filter(self, queryset, name, value):
        '''
        # Filter word in char (icontains)
        @name: default - 'search'
        @value: received from the request
        '''
        if value:        
            target_date = convert_string_to_date(value, DDMMYYY)
            if target_date:
                nearest_birthdays = queryset.annotate(
                    days_difference=ExpressionWrapper(
                        Abs(F('date') - target_date),
                        output_field=IntegerField(),
                    )
                ).order_by('days_difference')[:self.data.get('limit', 100)]

                nearest_ids = [actor.id for actor in nearest_birthdays]

                if nearest_ids:
                    queryset = queryset.filter(id__in=nearest_ids)

        else:
            queryset = queryset.filter(
                Q(name__icontains=value) |
                Q(place__icontains=value)
            )

        return queryset
