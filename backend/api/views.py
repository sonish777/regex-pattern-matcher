import csv
import io
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiParameter

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
        file = request.FILES.get('file')
        content_type = file.content_type
        if (content_type == 'text/csv'):
            file_content = file.read().decode('utf-8')
            io_string = io.StringIO(file_content)
            csv_reader = csv.reader(io_string, delimiter=',')

            headers = next(csv_reader) 
            rows = []
            for row in csv_reader:
                row_dict = dict(zip(headers, row))
                rows.append(row_dict)
            
            return Response({ 'status': 'success', 'data': rows }, status=201)