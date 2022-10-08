from django.urls import path
#from . import views
from .views import (
    # classroom views
    SchoolYearListView,
    ClassesListView,
    ClassDetailView,
    StudentProfileListView,
    StudentDetailsView,
    JoinClassView,

    # project views
    ClassProjectTopicsListView,
    ClassProjectsListView,
    ProjectCommentUpdateView,
    ProjectCommentDeleteView,
    CreateProjectStepOneView,
    CreateProjectStepTwoView,
    CreateProjectStepThreeView,
    CreateProjectStepFourView,
    CreateProjectStepFiveView,
    ProjectDetailView,
    EditProjectTextView,
    EditProjectAddVideoView,
    EditProjectAddLinkView,
    EditProjectAddPhotoView,
    ProjectConfirmDeleteView,
    ProjectDeleteView,
    ProjectVideoConfirmDeleteView,
    ProjectVideoDeleteView,
    ProjectPhotoConfirmDeleteView,
    ProjectPhotoDeleteView,
    ProjectCommentNotificationsDeleteView,

    # forum views
    ClassForumsListView
    )

urlpatterns = [
    # classroom urls
    path('find-classes/',SchoolYearListView.as_view(),name='classroom-findclasses'),
    path('find-classes/school-year/<int:pk>/',ClassesListView.as_view(),name='classroom-classes'),
    path('class-details/<str:class_title>/<int:pk>/',ClassDetailView.as_view(),name='classroom-classroom-details'),
    path('class-details/meet-the-team/<int:classroom_pk>/<str:classroom_title>/',StudentProfileListView,name='classroom-classroom-profiles'),
    path('class-project-topics/<int:pk>/',ClassProjectTopicsListView,name='classroom-project-topics'),
    path('class-projects/<int:pk>/',ClassProjectsListView,name='classroom-projects-list'),
    path('student-details/<int:profile_pk>/<int:classroom_pk>/',StudentDetailsView,name='classroom-student-details'),
    path('join-class/<int:classroom_pk>/',JoinClassView,name='classroom-join-class'),

    # project urls
    path('edit-comment/<int:pk>/',ProjectCommentUpdateView.as_view(),name='classroom-update-comment'),
    path('delete-comment/<int:pk>/',ProjectCommentDeleteView.as_view(),name='classroom-delete-comment'),
    path('create-project-step-1/<int:project_topic_pk>/',CreateProjectStepOneView,name='classroom-create-project-step-1'),
    path('create-project-step-2/<int:temp_project_pk>/',CreateProjectStepTwoView,name='classroom-create-project-step-2'),
    path('create-project-step-3/<int:temp_project_pk>/',CreateProjectStepThreeView,name='classroom-create-project-step-3'),
    path('create-project-step-4/<int:temp_project_pk>/',CreateProjectStepFourView,name='classroom-create-project-step-4'),
    path('create-project-step-5/<int:temp_project_pk>/',CreateProjectStepFiveView,name='classroom-create-project-step-5'),
    path('project-details/<int:project_pk>/',ProjectDetailView,name='classroom-project-details'),
    path('edit-project-text/<int:project_pk>/',EditProjectTextView,name='classroom-update-project'),
    path('add-project-video/<int:project_pk>/',EditProjectAddVideoView,name='classroom-add-video'),
    path('add-project-link/<int:project_pk>/',EditProjectAddLinkView,name='classroom-add-link'),
    path('add-project-photo/<int:project_pk>/',EditProjectAddPhotoView,name='classroom-add-project-photo'),
    path('confirm-delete-project/<int:project_pk>/',ProjectConfirmDeleteView,name='classroom-confirm-delete-project'),
    path('delete-project/<int:project_pk>/',ProjectDeleteView,name='classroom-delete-project'),
    path('confirm-delete-video/<int:project_pk>/<int:video_pk>/',ProjectVideoConfirmDeleteView,name='classroom-confirm-delete-video'),
    path('delete-project-video/<int:project_pk>/<int:video_pk>/',ProjectVideoDeleteView,name='classroom-delete-video'),
    path('confirm-delete-project-photo/<int:project_pk>/<int:project_photo_pk>/',ProjectPhotoConfirmDeleteView,name='classroom-confirm-delete-project-photo'),
    path('delete-project-photo/<int:project_pk>/<int:project_photo_pk>/',ProjectPhotoDeleteView,name='classroom-delete-project-photo'),
    path('delete-project-comment-notification/<int:notification_pk>/',ProjectCommentNotificationsDeleteView,name='classroom-project-comment-notification-delete'),
    
    # forum urls
    path('class-forums-list/<int:pk>/',ClassForumsListView,name='classroom-forums-list')
]