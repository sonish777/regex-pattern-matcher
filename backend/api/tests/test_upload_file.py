from io import BytesIO
from django.test import SimpleTestCase
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

class UploadFileTest(SimpleTestCase):

    def test_upload_csv(self):
        """Test that a valid csv file is uploaded successfully."""
        url = reverse('upload_file')

        csv_file_content = "name,age\nSonish,26\nJohn Doe, 26"
        csv_file = BytesIO(csv_file_content.encode())
        csv_file.name = 'test.csv'
        csv_file = InMemoryUploadedFile(csv_file, None, "test.csv", "text/csv", len(csv_file_content), None)

        response = self.client.post(url, { "file":  csv_file }, format="multipart")

        self.assertEqual(response.status_code, 201)
