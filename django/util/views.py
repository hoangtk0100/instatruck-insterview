from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, serializers
from .base import BaseResponse
from .messages import *

class EmptySerializer(serializers.Serializer):
    pass

class BaseView(viewsets.GenericViewSet):
    serializer_class = EmptySerializer

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_response(self, data=None, error_code=0, message='Success'):
        return BaseResponse(data=data, error_code=error_code, message=message).response()


