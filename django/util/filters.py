from .messages import START_YEAR_INVALID, END_YEAR_INVALID, END_YEAR_LESS_THAN_START_YEAR
from django_filters.rest_framework import FilterSet
from .exceptions import ValidationException
from django_filters import NumberFilter

class YearRangeFilter(FilterSet):
    start_year = NumberFilter(method='year_range_filter') 
    end_year = NumberFilter(method='year_range_filter')

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            if 'start_year' in data.keys() and data['start_year']:
                if int(data['start_year']) < 1900:
                    raise ValidationException(START_YEAR_INVALID)
            
            if 'end_year' in data.keys() and data['end_year']:
                if int(data['end_year']) < 1900:
                    raise ValidationException(END_YEAR_INVALID)

        super().__init__(data, *args, **kwargs)

    def year_range_filter(self, queryset, name, value):
        '''
        # Filter by date range
        @name: default - [start_year, end_year]
        @value: received from the request - format(YYYY-MM-DD)
        '''
        if (name == 'start_year') and value:
            return queryset.filter(year__gte=int(value))

        if (name == 'end_year') and value:
            value = int(value)
            start_year = self.data['start_year'] if 'start_year' in self.data.keys() else None
            if start_year and int(start_year) > value:
                raise ValidationException(END_YEAR_LESS_THAN_START_YEAR)

            return queryset.filter(year__lte=value)

class YearRangeParamsFilter(FilterSet):
    start_year = NumberFilter(method='year_range_filter') 
    end_year = NumberFilter(method='year_range_filter')

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            if data.get('start_year'):
                if int(data.get('start_year')) < 1900:
                    raise ValidationException(START_YEAR_INVALID)
            
            if data.get('end_year'):
                if int(data.get('end_year')) < 1900:
                    raise ValidationException(END_YEAR_INVALID)

        super().__init__(data, *args, **kwargs)

    def year_range_filter(self, queryset, name, value):
        '''
        # Filter by date range
        @name: default - [start_year, end_year]
        @value: received from the request - format(YYYY-MM-DD)
        '''
        if (name == 'start_year') and value:
            return queryset.filter(year__gte=int(value))

        if (name == 'end_year') and value:
            value = int(value)
            start_year = self.data.get('start_year') or None
            if start_year and int(start_year) > value:
                raise ValidationException(END_YEAR_LESS_THAN_START_YEAR)

            return queryset.filter(year__lte=value)

