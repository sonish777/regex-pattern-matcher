from io import BytesIO
from django.test import SimpleTestCase
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status


class UploadFileTest(SimpleTestCase):

    def setUp(self):
        csv_file_content = "name,email\nsonish,sonish@email.com\njoHn dOe, john@email.com"  # noqa: E501
        csv_file = InMemoryUploadedFile(BytesIO(csv_file_content.encode()),
                                        None,
                                        "test.csv",
                                        "text/csv",
                                        len(csv_file_content),
                                        None)

        invalid_file_content = b"Invalid file upload should fail!"
        invalid_file = InMemoryUploadedFile(file=BytesIO(invalid_file_content),
                                            field_name='file',
                                            name='invalid.txt',
                                            content_type='text/plain',
                                            size=len(invalid_file_content),
                                            charset=None)

        self.valid_file = csv_file
        self.invalid_file = invalid_file
        self.normalized_names = ["Sonish", "John Doe"]

    def test_upload_csv(self):
        """Test that a valid csv file is uploaded successfully."""
        url = reverse('upload_file')
        response = self.client.post(url,
                                    {"file": self.valid_file,
                                     "pattern": "Find numbers",
                                     "replacement": "***"},
                                    format="multipart")

        self.assertEqual(response.status_code, 201)

    def test_upload_invalid_file(self):
        """Test that uploading invalid file gives bad request"""
        url = reverse('upload_file')
        response = self.client.post(url, {'file': self.invalid_file,
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

    def test_regex_replacement(self):
        """Test that regex replacement works correctly"""
        replacement = "******@****.com"
        url = reverse('upload_file')
        response = self.client.post(url,
                                    {"file": self.valid_file,
                                     "pattern": "Find email addresses",
                                     "replacement": replacement},
                                    format="multipart")

        self.assertEqual(response.status_code, 201)
        response_data = response.data  # { status, data }
        self.assertEqual(response_data.get('data')[0]
                         .get('email'),
                         replacement)
        self.assertEqual(response_data.get('data')[1]
                         .get('email'),
                         replacement)

    def test_data_transformation(self):
        """Test that data transformation works correctly"""
        replacement = "******@****.com"
        url = reverse('upload_file')
        response = self.client.post(url,
                                    {"file": self.valid_file,
                                     "pattern": "Find email addresses",
                                     "replacement": replacement,
                                     "apply_transformations": True},
                                    format="multipart")

        self.assertEqual(response.status_code, 201)
        response_data = response.data  # { status, data }
        self.assertIn(response_data.get('data')[0]
                      .get('name'),
                      self.normalized_names)
        self.assertIn(response_data.get('data')[1]
                      .get('name'),
                      self.normalized_names)
