from django.test import TestCase
from django.urls import reverse

class MailClassifierViewTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse('mail-form'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spam Shield')

    def test_prediction_context_present(self):
        response = self.client.post(reverse('mail-form'), {'message': 'Win a free prize now'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('prediction', response.context)
        self.assertIn(response.context['prediction']['label'], {'Spam', 'Ham'})
