from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated


def user_login_required(func):
    """
    decorator to check if user is logged in with TokenAuthentication.
    """
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def wrapper_func(view, *args, **kwargs):
        return func(view, *args, **kwargs)
    return wrapper_func
