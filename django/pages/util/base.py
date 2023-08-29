from django.http import JsonResponse
from datetime import datetime
from pytz import utc

def get_utc_now():
    """
    Return current time in UTC.
    """
    return datetime.utcnow().replace(tzinfo=utc)

class BaseResponse:
    def __init__(self, data=None, error_code=0, message='Success'):
        self.data = data
        self.error_code = error_code
        self.message = message

    def response(self):
        return JsonResponse({
            "data": self.data,
            "error_code": self.error_code,
            "message": self.message,
            "currentTime": get_utc_now(),
        })
