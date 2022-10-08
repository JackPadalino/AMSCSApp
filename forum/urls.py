from django.urls import path
from .views import (
    # forum views
    ForumTopicsListView,
    QuestionsListView,
    AnswerNotificationDeleteView,
    RequestHelpfulNotificationView,
    ApproveDenyHelpfulRequestView,
    HelpfulNotificationDeleteView,
    # question views
    AskQuestionView,
    EditQuestionView,
    QuestionDetailsView,
    QuestionConfirmDeleteView,
    QuestionDeleteView,
    # answer views
    AnswerView,
    EditAnswerView,
    AnswerConfirmDeleteView,
    AnswerDeleteView,
    )

urlpatterns = [
    # forum urls
    path('topics-list/<int:pk>/',ForumTopicsListView,name='forum-topics-list'),
    path('questions-list/<int:forum_topic_pk>/',QuestionsListView,name='forum-questions-list'),
    path('delete-answer-notifcation/<int:notification_pk>/',AnswerNotificationDeleteView,name='forum-delete-answer-notification'),
    path('request-helpful-notification/<int:answer_pk>/',RequestHelpfulNotificationView,name='forum-request-helpful-notification'),
    path('delete-helpful-notifcation/<int:notification_pk>/',HelpfulNotificationDeleteView,name='forum-delete-helpful-notification'),
    path('approve-deny-helpful-request/<int:notification_pk>/<str:decision>/',ApproveDenyHelpfulRequestView,name='forum-approve-deny-helpful-request'),
    # question urls
    path('ask-new-question/<int:forum_topic_pk>/',AskQuestionView,name='forum-ask-new-question'),
    path('question-details/<int:question_pk>/',QuestionDetailsView,name='forum-question-details'),
    path('edit-question/<int:question_pk>/',EditQuestionView,name='forum-edit-question'),
    path('confirm-delete-question/<int:question_pk>/',QuestionConfirmDeleteView,name='forum-confirm-delete-question'),
    path('delete-question/<int:question_pk>/',QuestionDeleteView,name='forum-delete-question'),
    # answer urls
    path('answer-question/<int:question_pk>/',AnswerView,name='forum-answer-question'),
    path('edit-answer/<int:answer_pk>/',EditAnswerView,name='forum-edit-answer'),
    path('confirm-delete-answer/<int:answer_pk>/',AnswerConfirmDeleteView,name='forum-confirm-delete-answer'),
    path('delete-answer/<int:answer_pk>/',AnswerDeleteView,name='forum-delete-answer'),
    ]