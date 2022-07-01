import datetime
client = Client()
from django.test import Client, TestCase
from django.utils import timezone
from django.urls import reverse
from django.test.utils import setup_test_environment

from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('poll:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

class QuestionDetailViewTests(TestCase):
    def test_past_questions(self):
        past_question = create_question(question_text="Past question.", days =-5)
        url = reverse('poll:detail', args=(past_question.id,))
        response(self.client.get(url))
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('poll:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_future_question_and_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )
setup_test_environment()

response = client.get('/')
response = client.get(reverse('poll:index'))
response.context['latest_question_list']