from django.db.models import Model
from django.db import models

from api.helpers.constants import QuestionType


class Question(Model):
    text = models.CharField(max_length=2000,  blank=False, null=False)
    type = models.CharField(QuestionType, max_length=2000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        app_label = "api"
        db_table = "api_question"


class Answer(Model):
    text = models.CharField(max_length=2000, blank=False, null=False)
    question = models.ForeignKey("Question", null=True, on_delete=models.PROTECT, related_name="answers")
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        app_label = "api"
        db_table = "api_answer"
