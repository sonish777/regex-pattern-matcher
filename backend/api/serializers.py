from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class FileUploadSerializer(serializers.Serializer):
    ALLOWED_FILE_TYPES = ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']
    file = serializers.FileField()

    def validate_file(self, value):
        if not value:
            raise ValidationError("File is required.")
        
        if value.content_type not in self.ALLOWED_FILE_TYPES:
            raise ValidationError("File must be a Excel/CSV file.")
        
        return value
