from django.urls import path, include

from .views import *


urlpatterns = [
    path('', CourseListView.as_view(), name="course-list"),
    path('create/', CourseCreateView.as_view(), name='course-create'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
    path('task/create/<int:from_pk>/', TaskCreateView.as_view(), name='task-create'),
    path('task/update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/register/', CourseRegistrationView.as_view(), name='course-register'),
    path('answer/create/<int:from_pk>/', AnswerCreateView.as_view(), name='answer-create'),
    path('answer/update/<int:pk>/', AnswerUpdateView.as_view(), name='answer-update'),
    path('block/create/<int:from_pk>/', BlockCreateView.as_view(), name='block-create'),
    path('block/update/<int:pk>/', BlockUpdateView.as_view(), name='block-update'),
]
