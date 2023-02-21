from django.urls import path

from api.views.questions_views import QuestionView
from api.views.votes_views import votes_view

urlpatterns = [

    path("question", QuestionView.as_view()),
    path(
        "<int:question_id>/vote/<answer_id>", votes_view),

]
