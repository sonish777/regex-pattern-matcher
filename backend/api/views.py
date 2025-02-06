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

            return api_response(data=rows, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            return api_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Error: {str(e)}")
