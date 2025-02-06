from io import BytesIO
from django.test import SimpleTestCase
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status


class UploadFileTest(SimpleTestCase):

    def test_upload_csv(self):
        """Test that a valid csv file is uploaded successfully."""
        url = reverse('upload_file')

        csv_file_content = "name,age\nSonish,26\nJohn Doe, 26"
        csv_file = BytesIO(csv_file_content.encode())
        csv_file.name = 'test.csv'
        csv_file = InMemoryUploadedFile(csv_file,
                                        None,
                                        "test.csv",
                                        "text/csv",
                                        len(csv_file_content),
                                        None)

        response = self.client.post(url,
                                    {"file":  csv_file,
                                     "pattern": "Find numbers",
                                     "replacement": "***"},
                                    format="multipart")

        self.assertEqual(response.status_code, 201)

    def test_upload_invalid_file(self):
        """Test that uploading invalid file gives bad request"""
        url = reverse('upload_file')

        invalid_file_content = b"Invalid file upload should fail!"
        invalid_file = InMemoryUploadedFile(file=BytesIO(invalid_file_content),
                                            field_name='file',
                                            name='invalid.txt',
                                            content_type='text/plain',
                                            size=len(invalid_file_content),
                                            charset=None)

        response = self.client.post(url, {'file': invalid_file,
                                          "pattern": "Find numbers",
                                          "replacement": "***"},
                                    format="multipart")
        self.assertEqual(response.status_code,
                         status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    def test_missing_required_fields_error(self):
        """Test that missing required fields gives error response"""
        url = reverse('upload_file')
        response = self.client.post(url, {}, format="multipart")
        self.assertEqual(response.status_code,
                         status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("pattern", response.data.get('errors'))
        self.assertIn("replacement", response.data.get('errors'))
        self.assertIn("file", response.data.get('errors'))
