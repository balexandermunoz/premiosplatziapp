import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question
# TestCase is battery test
# Se testea modelos o vistas
class QuestionModelTest(TestCase):
    
    def setUp(self) -> None:
        self.question = Question(
            question_text = "¿Quién es el mejor Course Director de Platzi?"
            )
    
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is
        in the future"""
        self.question.pub_date = timezone.now() + datetime.timedelta(days=30)
        self.assertIs(self.question.was_published_recently(), False)
        
    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns True for questions whose pub_date is
        in the past and is 1 day ago from now"""
        self.question.pub_date = timezone.now() - datetime.timedelta(days=2)
        self.assertIs(self.question.was_published_recently(), False)
        
    def test_was_published_recently_with_now_questions(self):
        """was_published_recently returns True for questions whose pub_date is
        in same as now"""
        self.question.pub_date = timezone.now()
        self.assertIs(self.question.was_published_recently(), True)
        

def create_question(text, days):
    """
    Create a question with the given "question_text" and published the given
    number of days offset to now. (Negative for past, positive future)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=time)
class QuestionIndexViewText(TestCase):
    
    def setUp(self) -> None:
        self.no_display_question = Question(
            question_text="This text should not be displayed on the screen",
            pub_date=timezone.now() + datetime.timedelta(days=30)
            )
        self.display_question = Question(
            question_text="This text should be displayed on the screen",
            pub_date=timezone.now()
            )

    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index")) # Request http a polls:index
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are aviliable.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_no_future_questions(self):
        """No future questions are displayed"""
        self.no_display_question.save()
        response = self.client.get(reverse("polls:index"))
        self.assertNotContains(response, self.no_display_question.question_text)
        
    def test_right_question(self):
        """Displayed a right question"""
        self.display_question.save()
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, self.display_question.question_text)
        
    #### Class solution:
    def test_future_questions(self):
        """No display future questions"""
        create_question("Future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are aviliable.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_past_questions(self):
        """Display past questions"""
        question = create_question("Future question", -10)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, question.question_text)
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
        
    ####
        
    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past question are displayed
        """
        past_question = create_question(text="Past question", days=-30)
        future_question = create_question(text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )
    
    def test_two_past_questions(self):
        """The questions index page may display multiple questions"""
        past_question1 = create_question(text="Past question 1", days=-30)
        past_question2 = create_question(text="Past question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )
        
    def test_two_future_questions(self):
        """
        For two questions in the future, none is displayed
        """
        future_question1 = create_question(text="Future question 1", days=30)
        future_question2 = create_question(text="Future question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
class QuestionDetailViewTests(TestCase):
    
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns
        a 404 error not found
        """
        future_question = create_question(text="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past 
        displays the question's text
        """
        past_question = create_question(text="Past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
def create_choice(pk, choice_text, votes=0):
    """Create a choice that have pk of a specific question with the given 
    choice_text and votes."""
    question = Question.objects.get(pk)
    return question.choice_set.create(choice_text=choice_text, votes=votes)

class QuestionResultsViewTests(TestCase):
    
    def test_past_question(self):
        """Display the right text in results if there is a past question"""
        past_question = create_question("Past question", -15)
        response = self.client.get(
            reverse("polls:results", args=(past_question.id, ))
            )
        self.assertContains(response, past_question.question_text)
    
    def test_future_question(self):
        """Return 404 if there is a future question"""
        future_question = create_question("Future question", 15)
        response = self.client.get(
            reverse("polls:results", args=(future_question.id, ))
            )
        self.assertEqual(response.status_code, 404)
    
    def test_correct_votes(self):
        """Print the right quantity of votes in a question result"""
        past_question = create_question("Past question", -15)
        past_question.choice_set.create(choice_text="Choice 1", votes=2)
        past_question.choice_set.create(choice_text="Choice 2", votes=0)
        response = self.client.get(
            reverse("polls:results", args=(past_question.id, ))
            )
        self.assertContains(response, "Choice 1 -- 2 votes")
        self.assertContains(response, "Choice 2 -- 0 votes")
        
