from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import FileUploadSerializer
from .utils import api_response, process_csv, process_excel

@extend_schema(
    summary="Checks whether the API is running",
    responses={200: { "type": "object", "properties": { "status": { "type": "string" }}}}
)
@api_view(["GET"])
def health_check(request):
    return Response({ 'status': 'ok' })

@extend_schema(
        summary="Upload a CSV file for processing",
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'Upload a CSV/Excel file'
                    }
                }
            }
        }
)
@api_view(["POST"])
def upload_file(request):
    try:
        serializer = FileUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(errors=serializer.errors, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        file = serializer.validated_data.get('file')
        if file.name.lower().endswith('.csv'):
            rows = process_csv(file)
        else:
            rows = process_excel(file)
        return api_response(data=rows, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        print("ERROR IS ", str(e))
        return api_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Error: {str(e)}")