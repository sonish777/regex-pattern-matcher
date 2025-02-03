from django.http import JsonResponse
from rest_framework import status


def custom_404_handler(request, exception=None):
    return JsonResponse(
        {'status': '404', 'message': 'This endpoint does not exist. :('},
        status=status.HTTP_404_NOT_FOUND
    )
