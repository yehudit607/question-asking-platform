from django.test import TestCase
from rest_framework import status

from api.dto.question_dto import QuestionDto
from api.helpers.constants import QuestionType
from api.models import Question
from api.services.question_service import QuestionService


class QuestionServiceTestCase(TestCase):
    def setUp(self):
        self.question_data = {
            "text": "What is the capital of France?",
            "type": QuestionType.TRIVIA,
            "answers": [
                {"text": "Paris", "is_correct": True},
                {"text": "Madrid", "is_correct": False},
                {"text": "Berlin", "is_correct": False},
                {"text": "Rome", "is_correct": False},
            ],
        }

    def test_get_existing_question(self):
        question = Question.objects.create(text="What is the capital of Italy?", type=QuestionType.TRIVIA)
        dto = QuestionDto.from_record(question)

        result = QuestionService.get(question.id)

        self.assertEqual(result, dto)

    def test_get_non_existing_question(self):
        result = QuestionService.get(999)

        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("question with this id not found", result.json()["massage"])

    def test_create_question_with_multiple_correct_answers(self):
        self.question_data["answers"][0]["is_correct"] = True
        self.question_data["answers"][1]["is_correct"] = True

        with self.assertRaises(Exception) as cm:
            QuestionService.create(self.question_data)

        self.assertIn("There should be exactly one correct answer", str(cm.exception))

    def test_create_question_successfully(self):
        question_id = QuestionService.create(self.question_data)

        question = Question.objects.get(id=question_id)
        self.assertEqual(question.text, self.question_data["text"])
        self.assertEqual(question.type, self.question_data["type"])

        answers = question.answers.all().order_by("id")
        self.assertEqual(len(answers), len(self.question_data["answers"]))

        for i, ans in enumerate(answers):
            self.assertEqual(ans.text, self.question_data["answers"][i]["text"])
            self.assertEqual(ans.is_correct, self.question_data["answers"][i]["is_correct"])
