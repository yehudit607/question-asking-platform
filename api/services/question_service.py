from http import HTTPStatus

from django.db import transaction
from django.http import JsonResponse

from api.dto.question_dto import QuestionDto
from api.helpers.base_helpers import get_session_logger, question_exception, QuestionException
from api.helpers.constants import QuestionType
from api.models import Question, Answer

logger = get_session_logger()


class QuestionService:
    model = Question
    dto = QuestionDto

    @classmethod
    def get(
        cls,
        question_id: int,
    ):
        logger.debug(
            f"Get metadata for question  id:{question_id} "
        )
        question = cls.model.objects.filter(id=question_id).first()       # filter only the custom forms for the requested user.
        if not question:
            logger.debug(
                f"question with this id not found. id: {question_id}"
            )
            return JsonResponse(

                data={"message": f"question with this id not found. id: {question_id}"},
                status=HTTPStatus.NOT_FOUND,
            )

        return cls.dto.from_record(question)

    @classmethod
    def create(cls, question_data: dict) -> int:
        logger.debug(
            f"Creating a new question.."
        )
        if question_data.get("type") is QuestionType.TRIVIA:
            correct_answers = [answer for answer in question_data['answers'] if answer['is_correct']]
            if len(correct_answers) != 1:
                raise QuestionException(
                    "There should be exactly one correct answer",
                    HTTPStatus.BAD_REQUEST,
                )
        with transaction.atomic():
            question = Question(
                text=question_data.get("text"),
                type=question_data.get("type")
            )
            question.save()
            answers = question_data.get("answers")
            for ans in answers:
                answer = Answer(text=ans.get("text"), is_correct=ans.get("is_correct"), question=question)
                answer.save()

            logger.debug(f"question successfully created with id:. {question.id}.")

        return question.id
