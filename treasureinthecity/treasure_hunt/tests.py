from django.test import TestCase
from django.urls import reverse
from .models import PuzzleCity, Place

class AnswerTest(TestCase):
    fixtures = ['test.json', ]

    def test_answer(self):
        PuzzleCitys = PuzzleCity.objects.all()
        #any place for test (logs)
        place = Place.objects.first()
        for pc in PuzzleCitys:
            # Test call view with good answer
            data = {
                'answer_input': pc.answer
            }
            response = self.client.post(reverse('answer', args=[pc.id, place.id]), data)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'true')
            # Test call view with wrong answer
            data = {
                'answer_input': 'wrong_answer_xxxx'
            }
            response = self.client.post(reverse('answer', args=[pc.id, place.id]), data)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'false')
            # Test call view with wrong answer
