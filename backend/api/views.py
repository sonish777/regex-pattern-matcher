from uuid import uuid4
from drf_spectacular.utils import OpenApiParameter
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import FileUploadSerializer
from .utils import api_response, process_csv, process_excel
from llm.services import LLMService
from .services import RegexParserService, DataTransformationService


class HealthCheckView(APIView):
    @extend_schema(
        summary="Checks whether the API is running",
        responses={200:
                   {"type": "object", "properties":
                    {"status": {"type": "string"}}}}
    )
    def get(self, request):
        return Response({'status': 'ok'})


class UploadAndProcessView(APIView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.llm_service = LLMService()
        self.regex_parser_service = RegexParserService()
        self.data_transformation_service = DataTransformationService()

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
                    },
                    'pattern': {
                        'type': 'string',
                        'required': 'true'
                    },
                    'replacement': {
                        'type': 'string',
                        'required': 'true'
                    }
                }
            }
        }
    )
    def post(self, request):
        try:
            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return api_response(
                    errors=serializer.errors,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

            file = serializer.validated_data.get('file')
            pattern = serializer.validated_data.get('pattern')
            replacement = serializer.validated_data.get('replacement')

            session_id = uuid4()
            rows = process_csv(file) \
                if file.name.lower().endswith('.csv') \
                else process_excel(file)
            if not rows:
                return api_response(data=[],
                                    status_code=status.HTTP_201_CREATED)
            headers = list(rows[0].keys())
            llm_response = self.llm_service \
                .generate_regex_from_description(pattern, headers)
            if not llm_response:
                return api_response(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    error="Couldn't not generate regex from description.")
            rows = self.regex_parser_service \
                .parse(llm_response) \
                .apply_replacement(rows=rows, replacement=replacement.strip())
            if serializer.validated_data.get("apply_transformations"):
                llm_transformation_response = self.llm_service \
                    .suggest_transformations(headers)
                if llm_transformation_response:
                    rows = self.data_transformation_service \
                        .parse(llm_transformation_response) \
                        .apply_transformations(rows)
            cache.set(session_id, rows, timeout=60*60)
            response_data = {
                "total": len(rows),
                "total_pages": round(len(rows)/5),
                "page": 0,  # 0 indexed page
                "page_size": 5,
                "rows": rows[0:5]
            }
            return api_response(data=response_data,
                                session_id=session_id,
                                status_code=status.HTTP_201_CREATED)
        except Exception as e:
            return api_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Error: {str(e)}")


class GetProcessedDataView(APIView):

    @extend_schema(
        summary="Get the processed data with pagination",
        parameters=[
            OpenApiParameter(
                name="session_id",
                description="UUID session ID of the processed data",
                required=True,
                type=str
            ),
            OpenApiParameter(
                name="page",
                description="Page number for pagination",
                required=False,
                type=int,
                default=1
            ),
            OpenApiParameter(
                name="page_size",
                description="Page size for pagination",
                required=False,
                type=int,
                default=5
            )
        ],
        responses={200:
                   {"type": "object", "properties":
                    {"total": {"type": "integer"},
                     "session_id": {"type": "string"},
                     "data": {"type": "array", "items": {"type": "object"}}}}}
    )
    def get(self, request):
        try:
            session_id = request.query_params.get('session_id')
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))

            if not session_id:
                return api_response(
                    status_code=status.HTTP_404_NOT_FOUND,
                    error="The requested resource was not found.")

            processed_data = cache.get(session_id)

            if not processed_data:
                return api_response(
                    status_code=status.HTTP_404_NOT_FOUND,
                    error="The requested resource was not found.")

            start_index = page * page_size  # page 0 indexed
            end_index = (page + 1) * page_size
            data = processed_data[start_index:end_index]

            paginated_response = {
                "total": len(processed_data),
                "total_pages": round(len(processed_data)/page_size),
                "page": page,
                "page_size": page_size,
                "rows": data
            }
        except Exception as e:
            return api_response(error=str(e),
                                status_code=status.
                                HTTP_500_INTERNAL_SERVER_ERROR)

        return api_response(data=paginated_response, session_id=session_id)
