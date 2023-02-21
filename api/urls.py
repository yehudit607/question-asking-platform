from django.urls import path

from api.views import QuestionView, votes_view

urlpatterns = [

    path("question", QuestionView.as_view()),
    path(
        "<int:question_id>/vote/<answer_id>", votes_view),

]
