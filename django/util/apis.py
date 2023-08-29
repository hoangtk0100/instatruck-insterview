import functools
from .base import BaseResponse
from .exceptions import BaseException, InvalidArgumentException
from .messages import CONTACT_ADMIN_FOR_SUPPORT, INVALID_ARGUMENT, FIELD_NOT_SUPPORT, NEGATIVE_PAGE_SIZE
from django.core.exceptions import ValidationError, FieldError
from django.core.paginator import Paginator
import logging
LOGGER = logging.getLogger(__name__)

def handle_exceptions(exception):
    if isinstance(exception, BaseException):
        return exception.to_dict()
    else:
        default_response = BaseResponse(data=None, error_code=500, message=CONTACT_ADMIN_FOR_SUPPORT)
        switcher = {
            ValidationError: BaseResponse(data=None, error_code=400, message=INVALID_ARGUMENT),
            ValueError: BaseResponse(data=None, error_code=400, message=str(exception)),
            FieldError: BaseResponse(data=None, error_code=400, message=FIELD_NOT_SUPPORT),
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

PAGE_SIZE=10

def paginate_data(request, data):
    '''
    Function to handle pagination data.

    Params:

    data: array data.

    request: request object that contain paginate info

    page: page to show (Default is 1).

    page_size: Defaults is 10 (PAGE_SIZE=10).
    
    Return a JSON data:

    response_data = {
        "page": page_number,
        "limit": page_size,
        "total": total,
        "total_pages": total_pages,
        "content": content,
    }
    '''

    page = int(request.GET.get('page') or request.data.get('page') or 1)
    limit = int(request.GET.get('limit') or request.data.get('limit') or PAGE_SIZE)

    # Handle page_size = 'all'
    # page_size = 0 for get all
    if limit == 0:
        limit = len(data) + 1
    elif limit < 0:
        raise InvalidArgumentException(NEGATIVE_PAGE_SIZE)

    paginator = Paginator(data, limit)

    total_pages = paginator.num_pages

    if int(total_pages) < page:
        page_number = page
        content = []
    else:
        current_page = paginator.page(page)
        page_number = current_page.number
        content = current_page.object_list

    total = paginator.count

    return {
        "page": page_number,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "content": content,
    }
