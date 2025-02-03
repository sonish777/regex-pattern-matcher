from django.test import SimpleTestCase
from django.urls import reverse


class HeathCheckTest(SimpleTestCase):

    def test_health_check(self):
        """Test that health check return status ok JSON response."""
        url = reverse('health_check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'ok'})
