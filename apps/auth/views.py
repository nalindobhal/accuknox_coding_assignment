from django.contrib.auth import authenticate, login
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView

from apps.auth.data_validator import LoginRequestValidator, SignupRequestValidator
from apps.auth.utils import get_auth_token
from apps.base.views import ErrorJsonResponse, SuccessJsonResponse
from apps.user.serializers import UserSerializer


@api_view(['POST'])
def login_view(request):
    """
    Login view using FBV
    """
    try:
        req = LoginRequestValidator(data=request.data)
        if not req.is_valid():
            return ErrorJsonResponse(data={
                "status": "error",
                "message": req.errors
            })
        user = authenticate(request, email=req.validated_data.get('email'), password=req.validated_data.get('password'))
        if user and user.is_active:
            login(request, user)
            return SuccessJsonResponse(data={
                "status": "ok",
                "token": get_auth_token(user),
                "user": UserSerializer(instance=user).data
            })
        else:
            return ErrorJsonResponse(data={
                "status": "error",
                "message": "Cannot login, contact admin"
            })
    except serializers.ValidationError as e:
        return ErrorJsonResponse(data={
            "error": e.detail
        })


class SignupView(CreateAPIView):
    """
    signup view using CBV, generic CreateAPIView
    """
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            req = SignupRequestValidator(data=request.data)
            if not req.is_valid():
                return ErrorJsonResponse(data={
                    "status": "error",
                    "message": req.errors
                })

            user_serializer = UserSerializer(data=req.validated_data)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return ErrorJsonResponse({"status": "error", "error": user_serializer.errors})

            user = authenticate(
                request, email=req.validated_data.get('email'), password=req.validated_data.get('password')
            )
            if user and user.is_active:
                login(request, user)
                return SuccessJsonResponse(data={
                    "status": "ok",
                    "token": get_auth_token(user),
                    "user": user_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return ErrorJsonResponse(data={
                    "status": "error",
                    "message": "Cannot login, contact admin"
                })
        except serializers.ValidationError as e:
            return ErrorJsonResponse(data={
                "error": e.detail
            })
