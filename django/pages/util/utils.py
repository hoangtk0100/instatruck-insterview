import functools
from .base import BaseResponse
from .exceptions import BaseException
from django.core.exceptions import ValidationError, FieldError
import logging
LOGGER = logging.getLogger(__name__)

def handle_exceptions(exception):
    if isinstance(exception, BaseException):
        return exception.to_dict()
    else:
        default_response = BaseResponse(data=None, error_code=500, message='CONTACT_ADMIN_FOR_SUPPORT')
        switcher = {
            ValidationError: BaseResponse(data=None, error_code=400, message='INVALID_ARGUMENT'),
            ValueError: BaseResponse(data=None, error_code=400, message=str(exception)),
            FieldError: BaseResponse(data=None, error_code=400, message='FIELD_NOT_SUPPORT'),
        }

        response = switcher.get(type(exception), default_response)
        if response.error_code == 500 or type(exception) in [ValidationError, ValueError, FieldError]:
            LOGGER.error("=== Exception details:", exc_info=True)

        return response


def catch_exceptions(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs).response()
        except Exception as exception:
            return handle_exceptions(exception).response()

    return func