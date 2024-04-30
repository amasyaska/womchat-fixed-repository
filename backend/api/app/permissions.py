from rest_framework import permissions, status
from rest_framework.exceptions import APIException

class IsNotAuthenticated(permissions.BasePermission):
    message = "Authenticated users can't register new account."

    def has_permission(self, request, view):
        if view.get_view_name() == 'User Authenticate':
            self.message = "Authenticated users can't login to another account."
        return not request.user.is_authenticated
    

class GenericAPIException(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'

    def __init__(self, detail=None, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class CustomIsAuthenticated(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise GenericAPIException(detail="User isn't authenticated.", status_code=401)
        return True