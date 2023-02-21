from rest_framework import serializers
from api.helpers.constants import QuestionType


class AnswerSchemas(serializers.Serializer):
    text = serializers.CharField(required=True)
    is_correct = serializers.BooleanField(required=False)


class QuestionSchemas(serializers.Serializer):

    text = serializers.CharField(required=True)
    type = serializers.ChoiceField(choices=QuestionType.values(), required=True)
    answers = AnswerSchemas(many=True)
