from typing import Optional

class BaseException(Exception):
    STATUS_CODE = 500
    DEFAULT_MESSAGE_CODE = "CONTACT_ADMIN_FOR_SUPPORT"
    MESSAGE = "CONTACT_ADMIN_FOR_SUPPORT"

    def __init__(self, message = "CONTACT_ADMIN_FOR_SUPPORT", message_code: Optional[str] = None, error_code: Optional[str] = None, **kwargs):
        self.error_code = error_code or self.STATUS_CODE
        self.message_code = message_code or self.DEFAULT_MESSAGE_CODE
        self.message = message or self.MESSAGE

    def to_dict(self):
        return {"error_code": self.error_code, "message_code": self.message_code, "message": self.message}

    def __str__(self):
        return f"[{self.message_code}] - {self.message}"


class AuthenticationException(BaseException):
    STATUS_CODE = 401
    DEFAULT_MESSAGE_CODE = "PERMISSION_DENIED"
    MESSAGE = "PERMISSION_DENIED"

    def __init__(self, message = "PERMISSION_DENIED"):
        self.MESSAGE = message


class InvalidArgumentException(BaseException):
    STATUS_CODE = 400
    DEFAULT_MESSAGE_CODE = "INVALID_ARGUMENT"
    MESSAGE = "INVALID_ARGUMENT"

    def __init__(self, message = "INVALID_ARGUMENT"):
        self.MESSAGE = message


class NotFoundException(BaseException):
    STATUS_CODE = 404
    DEFAULT_MESSAGE_CODE = "NOT_FOUND_EXCEPTION"
    MESSAGE = "NOT_FOUND_EXCEPTION"

    def __init__(self, message = "NOT_FOUND_EXCEPTION"):
        self.MESSAGE = message


class NetworkException(BaseException):
    STATUS_CODE = 500
    DEFAULT_MESSAGE_CODE = "NETWORK_EXCEPTION"
    MESSAGE = "NETWORK_EXCEPTION"

    def __init__(self, message = "NETWORK_EXCEPTION"):
        self.MESSAGE = message


class ValidationException(BaseException):
    STATUS_CODE = 400
    DEFAULT_MESSAGE_CODE = "VALIDATION_EXCEPTION"
    MESSAGE = "VALIDATION_EXCEPTION"

    def __init__(self, message = "VALIDATION_EXCEPTION"):
        self.MESSAGE = message


class PermissionDenied(BaseException):
    STATUS_CODE = 403
    DEFAULT_MESSAGE_CODE = "PERMISSION_DENIED"
    MESSAGE = "PERMISSION_DENIED"

    def __init__(self, message = "PERMISSION_DENIED"):
        self.MESSAGE = message
