from http import HTTPStatus

from django.db.models import F
from django.http import JsonResponse

from api.helpers.base_helpers import get_session_logger, question_exception
from api.helpers.constants import QuestionType
from api.models import Question, Answer

logger = get_session_logger()


class VoteService:
    model = Answer

    @classmethod
    def vote(cls, question_id: int, answer_id: int):
        answer = Answer.objects.filter(id=answer_id).first()
        if not answer:
            logger.debug(
                f"answer with this id not found. id: {answer_id}"
            )
            return JsonResponse(
                data={"message": f"answer with this id not found. id: {answer_id}"},
                status=HTTPStatus.NOT_FOUND,
            )
        answer.votes = F('votes') + 1
        answer.save()
        answer.refresh_from_db()
        is_correct = (answer.is_correct
                      if answer.question.type == QuestionType.TRIVIA.value
                      else None)
        return answer.votes, is_correct
