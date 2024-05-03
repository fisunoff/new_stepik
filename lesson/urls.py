from django.urls import path, include

from .views import *


urlpatterns = [
    path('', CourseListView.as_view(), name="course-list"),
    path('create/', CourseCreateView.as_view(), name='course-create'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
    path('<int:pk>/register/', CourseRegistrationView.as_view(), name='course-register'),
    path('answer/create/<int:from_pk>/', AnswerCreateView.as_view(), name='answer-create'),
    path('answer/update/<int:pk>/', AnswerUpdateView.as_view(), name='answer-update'),
]
