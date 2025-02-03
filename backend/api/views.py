import csv
import io
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import FileUploadSerializer
from .utils import api_response

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
    if request.method == 'POST':
        try:
            serializer = FileUploadSerializer(data=request.data)
            if (serializer.is_valid()):
                file = serializer.validated_data.get('file')
                file_content = file.read().decode('utf-8')
                io_string = io.StringIO(file_content)
                csv_reader = csv.reader(io_string, delimiter=',')
                headers = next(csv_reader) 
                rows = []
                for row in csv_reader:
                    row_dict = dict(zip(headers, row))
                    rows.append(row_dict)
                return api_response(data=rows, status_code=status.HTTP_201_CREATED)
            return api_response(errors=serializer.errors, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return api_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Error: {str(e)}")