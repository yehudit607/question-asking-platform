from http import HTTPStatus
from django.http import JsonResponse
from rest_framework.decorators import api_view
from api.services.votes_service import VoteService


@api_view(["GET"])
#@is_logged_in
def votes_view(request, question_id, answer_id):
    votes, is_correct = VoteService.vote(question_id, answer_id)
    message = {"votes": votes}
    if is_correct is not None:
        message["is_correct"] = is_correct
    return JsonResponse(
                data=message,
                status=HTTPStatus.OK,
                safe=False,
            )