from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from rest_framework import status


class SuccessJsonResponse(JsonResponse):
    def __init__(
            self,
            data,
            encoder=DjangoJSONEncoder,
            safe=True,
            json_dumps_params=None,
            **kwargs,
    ):

        super().__init__(data, **kwargs)


class ErrorJsonResponse(JsonResponse):
    def __init__(
            self,
            data,
            encoder=DjangoJSONEncoder,
            safe=True,
            json_dumps_params=None,
            **kwargs,
    ):

        kwargs['status'] = status.HTTP_400_BAD_REQUEST
        super().__init__(data, **kwargs)
