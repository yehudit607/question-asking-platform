from http import HTTPStatus
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api.dto.question_dto import QuestionDto
from api.helpers.base_helpers import get_session_logger, question_exception, QuestionException, general_exception, \
    is_logged_in
from api.helpers.constants import QuestionType
from api.scheamas.question_schema import QuestionSchemas
from api.serializers.question_serializer import QuestionSerializer
from api.services import question_service
from api.services.question_service import QuestionService
from api.services.votes_service import VoteService

logger = get_session_logger()


class QuestionView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get(self, request, **kwargs):
        try:
            question_id = request.query_params.get("question_id")
            if not question_id:
                raise QuestionException("Question ID is required", HTTPStatus.BAD_REQUEST)
            response = self.retrieve(question_id)
            return JsonResponse(
                QuestionSerializer(response).data,
                status=HTTPStatus.OK,
                safe=False,
            )
        except QuestionException as ex:
            return question_exception(ex)

        except Exception as ex:
            return general_exception()


    def retrieve(
        self, question_id
    ):
        return QuestionService.get(
            question_id
        )

    def create(self, request, *args, **kwargs):
        try:
            question_schema = QuestionSchemas(data=request.data)
            if question_schema.is_valid():
                question_data = question_schema.data
                question_id = self.mapping_and_create(question_data)
            else:
                raise QuestionException(
                    f"Schem is not valid with errors: {question_schema.errors}",
                    HTTPStatus.BAD_REQUEST,
                )
            return JsonResponse(
                data={"question_id": question_id},
                status=HTTPStatus.OK,
                safe=False,
            )

        except QuestionException as ex:
            return question_exception(ex)

        except Exception as ex:
            return general_exception()

    def mapping_and_create(self, question_data):
        question_id = QuestionService.create(question_data)
        return question_id


@api_view(["GET"])
#@is_logged_in
def votes_view(request, question_id, answer_id):
    votes, is_correct = VoteService.vote(question_id, answer_id)
    massage = {"votes": votes}
    if is_correct is not None:
        massage["is_correct"] = is_correct
    return JsonResponse(
                data=massage,
                status=HTTPStatus.OK,
                safe=False,
            )


