from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value:
            raise ValidationError("File is required.")
        
        if value.content_type != "text/csv":
            raise ValidationError("File must be a Excel/CSV file.")
        
        return value
