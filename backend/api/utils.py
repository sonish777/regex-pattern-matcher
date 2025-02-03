# utils.py

from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

def api_response(data=None, error=None, errors=None, status_code=status.HTTP_200_OK):
    """Utility function to standardize API responses."""
    if status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
        response_data = {
            "status": "error",
            "errors": errors
        }
    elif status_code >= status.HTTP_400_BAD_REQUEST:
        response_data = {
            "status": "error",
            "error": error
        }
    else:
        response_data = {
            "status": "success",
            "data": data or [],
        }
    return Response(response_data, status=status_code)

